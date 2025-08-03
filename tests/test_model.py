import requests

def test_api_predict():
    url = "https://16h3b2a35d.execute-api.us-east-1.amazonaws.com/predict"
    headers = {"Authorization": "Bearer secret-token-123"}
    sample = {
        "Annual_Income": 0,
        "Monthly_Inhand_Salary": 0,
        "Num_Bank_Accounts": 0,
        "Num_Credit_Card": 0,
        "Interest_Rate": 0,
        "Num_of_Loan": 0,
        "Delay_from_due_date": 0,
        "Num_of_Delayed_Payment": 0,
        "Changed_Credit_Limit": 0,
        "Num_Credit_Inquiries": 0,
        "Credit_Utilization_Ratio": 0,
        "Outstanding_Debt": 0,
        "Monthly_Balance": 0,
        "Age": 0,
        "Total_EMI_per_month": 0,
        "Type_of_Loan": "string",
        "Payment_Behaviour": "string",
        "Amount_invested_monthly": 0,
        "Credit_Mix": "string",
        "Payment_of_Min_Amount": "string",
        "Credit_History_Age": "string",
        "Occupation": "string"
    }
    res = requests.post(url, json=sample, headers=headers)
    assert res.status_code == 200
    assert res.json()["score"] in ["Good", "Standard", "Poor"]
