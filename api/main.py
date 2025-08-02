import os
import boto3
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from api.schemas import InputData
from mangum import Mangum

# Parâmetros de configuração
BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "quantumfinance-mlflow-artifacts")
MODEL_KEY = os.getenv("MODEL_KEY", "models/model_latest.pkl")
LOCAL_PATH = "/tmp/model.pkl"

app = FastAPI()

# Inicializa o modelo
model = None
try:
    print("📥 Baixando modelo do S3...")
    boto3.client("s3").download_file(BUCKET_NAME, MODEL_KEY, LOCAL_PATH)
    model = joblib.load(LOCAL_PATH)
    print("✅ Modelo carregado com sucesso!")
except Exception as e:
    print("❌ Erro ao carregar modelo do S3:", e)

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
