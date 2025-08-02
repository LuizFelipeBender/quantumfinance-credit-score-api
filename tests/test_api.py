import importlib
import os
import sys
from unittest.mock import patch

from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


class DummyModel:
    def predict(self, df):
        return ["Good"]


def create_client():
    with patch.dict(os.environ, {"MLFLOW_TRACKING_URI": "http://fake"}):
        with patch("mlflow.sklearn.load_model", return_value=DummyModel()):
            import api.main
            importlib.reload(api.main)
            return TestClient(api.main.app)


def sample_payload():
    return {
        "Annual_Income": 48000.0,
        "Monthly_Inhand_Salary": 3800.0,
        "Num_Bank_Accounts": 2,
        "Num_Credit_Card": 1,
        "Interest_Rate": 15.0,
        "Num_of_Loan": 1,
        "Delay_from_due_date": 4,
        "Num_of_Delayed_Payment": 2.0,
        "Changed_Credit_Limit": 1200.0,
        "Num_Credit_Inquiries": 2.0,
        "Credit_Utilization_Ratio": 34.5,
        "Outstanding_Debt": 1600.0,
        "Monthly_Balance": 2500.0,
        "Age": 29,
    }


def test_predict_authorized():
    client = create_client()
    headers = {"Authorization": "Bearer secret-token-123"}
    res = client.post("/predict", json=sample_payload(), headers=headers)
    assert res.status_code == 200
    assert res.json()["score"] in ["Good", "Standard", "Poor"]


def test_predict_unauthorized():
    client = create_client()
    headers = {"Authorization": "Bearer invalid"}
    res = client.post("/predict", json=sample_payload(), headers=headers)
    assert res.status_code == 401
