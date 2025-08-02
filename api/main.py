import os
import pandas as pd
import joblib
import boto3
import tempfile
import mlflow
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from mangum import Mangum
from schemas import InputData
from fastapi.responses import FileResponse


# MLflow tracking URI
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# Inicializa FastAPI
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

# Função para carregar modelo do S3
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

# Carrega o modelo na inicialização
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

# Healthcheck
@app.get("/")
def health():
    return {"status": "ok"}


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    favicon_path = os.path.join(os.path.dirname(__file__), "favicon.ico")
    if os.path.exists(favicon_path):
        return FileResponse(favicon_path)
    return {}


# Endpoint de predição
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

        # Validação de colunas esperadas
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


# Lambda handler para AWS
handler = Mangum(app)

# Execução local
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

