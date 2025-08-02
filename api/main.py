import os
import pandas as pd
import mlflow
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from api.schemas import InputData, PredictionOutput
from api.auth import get_current_user
from mangum import Mangum

# Configurações do MLflow
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
MODEL_NAME = os.getenv("MODEL_NAME", "quantumfinance-credit-score-model")
MODEL_STAGE = os.getenv("MODEL_STAGE", "Production")

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

app = FastAPI()


def load_production_model():
    """Tenta carregar o modelo registrado em Production."""
    try:
        return mlflow.sklearn.load_model(f"models:/{MODEL_NAME}/{MODEL_STAGE}")
    except Exception as e:
        print(f"❌ Erro ao carregar modelo do MLflow: {e}")
        return None


model = load_production_model()


def get_model():
    global model
    if model is None:
        model = load_production_model()
    return model


@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionOutput)
async def predict(data: InputData, user: str = Depends(get_current_user)):
    model = get_model()
    if model is None:
        raise HTTPException(status_code=500, detail="Modelo não disponível")
    try:
        df = pd.DataFrame([data.dict()])
        pred = model.predict(df)[0]
        return {"score": str(pred)}
    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})


handler = Mangum(app)
