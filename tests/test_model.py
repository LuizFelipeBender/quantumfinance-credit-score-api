import requests

def test_api_predict():
    url = "http://localhost:8000/predict"
    headers = {"Authorization": "Bearer secret-token-123"}
    sample = {
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
        "Age": 29
    }
    res = requests.post(url, json=sample, headers=headers)
    assert res.status_code == 200
    assert res.json()["score"] in ["Good", "Standard", "Poor"]
