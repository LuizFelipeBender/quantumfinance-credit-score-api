
import mlflow
import mlflow.sklearn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from api.schemas import InputData
import pandas as pd
import os
from mangum import Mangum

mlflow.set_registry_uri(os.environ.get("MLFLOW_S3_URI"))

app = FastAPI()

try:
    model = mlflow.sklearn.load_model("models:/QuantumCreditScoreModel/Production")
except Exception as e:
    model = None
    print("Erro ao carregar modelo do MLflow:", e)

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/predict")
async def predict(data: InputData, request: Request):
    if model is None:
        raise HTTPException(status_code=500, detail="Modelo não disponível")
    try:
        df = pd.DataFrame([data.dict()])
        pred = model.predict(df)[0]
        return {"score_class": int(pred)}
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})

handler = Mangum(app)
