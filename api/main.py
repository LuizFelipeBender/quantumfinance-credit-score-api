import os
import pandas as pd
import joblib
import boto3
import tempfile
import mlflow
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from mangum import Mangum
from fastapi.responses import FileResponse
from pydantic import BaseModel

# Definição da classe InputData diretamente aqui
class InputData(BaseModel):
    Annual_Income: float
    Monthly_Inhand_Salary: float
    Num_Bank_Accounts: int
    Num_Credit_Card: int
    Interest_Rate: float
    Num_of_Loan: int
    Delay_from_due_date: int
    Num_of_Delayed_Payment: float
    Changed_Credit_Limit: float
    Num_Credit_Inquiries: float
    Credit_Utilization_Ratio: float
    Outstanding_Debt: float
    Monthly_Balance: float
    Age: int
    Total_EMI_per_month: float
    Type_of_Loan: str
    Payment_Behaviour: str
    Amount_invested_monthly: float
    Credit_Mix: str
    Payment_of_Min_Amount: str
    Credit_History_Age: str
    Occupation: str

# Configurações MLflow
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

app = FastAPI()

# Segurança via Bearer Token
security = HTTPBearer()
SECRET_TOKEN = {
    "secret-token-123": "parceiro_a",
    "secret-token-456": "parceiro_b"
}

# Parâmetros do S3
S3_BUCKET = "quantumfinance-mlflow-artifacts"
S3_KEY = "models/model_latest.pkl"

def load_model_from_s3():
    try:
        s3 = boto3.client("s3")
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            s3.download_fileobj(S3_BUCKET, S3_KEY, tmp)
            tmp_path = tmp.name
        print(f"✅ Modelo carregado de {S3_BUCKET}/{S3_KEY}")
        return joblib.load(tmp_path)
    except Exception as e:
        print(f"❌ Erro ao carregar modelo do S3: {e}")
        return None

model = load_model_from_s3()
expected_columns = None

if model:
    try:
        if hasattr(model, "feature_names_in_"):
            expected_columns = list(model.feature_names_in_)
        elif hasattr(model, "named_steps") and hasattr(model.named_steps, "preprocessor"):
            expected_columns = model.named_steps["preprocessor"].get_feature_names_out().tolist()
        print("📊 Colunas esperadas pelo modelo:", expected_columns)
    except Exception as e:
        print("⚠️ Não foi possível identificar colunas esperadas:", e)

@app.get("/")
def health():
    return {"status": "ok"}

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    favicon_path = os.path.join(os.path.dirname(__file__), "favicon.ico")
    if os.path.exists(favicon_path):
        return FileResponse(favicon_path)
    return {}

@app.post("/predict")
def predict(
    input: InputData,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    if token not in SECRET_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

    if not model:
        raise HTTPException(status_code=500, detail="Modelo indisponível")

    try:
        data = pd.DataFrame([input.dict()])

        if expected_columns:
            missing = set(expected_columns) - set(data.columns)
            if missing:
                raise HTTPException(status_code=400, detail=f"columns are missing: {missing}")

        prediction = model.predict(data)[0]
        return {"score": str(prediction)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/models")
def list_models(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if token not in SECRET_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        s3 = boto3.client("s3")
        response = s3.list_objects_v2(Bucket=S3_BUCKET, Prefix="models/")
        files = [obj["Key"] for obj in response.get("Contents", []) if obj["Key"].endswith(".pkl")]
        return {"available_models": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar modelos: {str(e)}")

@app.get("/ping")
def ping():
    return {"message": "pong"}

# Handler AWS Lambda com Mangum
handler = Mangum(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
