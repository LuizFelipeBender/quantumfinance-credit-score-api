import requests

def test_api_predict():
    url = "https://16h3b2a35d.execute-api.us-east-1.amazonaws.com/predict"
    headers = {"Authorization": "Bearer secret-token-123"}
    sample =    {
    "Annual_Income": 10000.0,
    "Monthly_Inhand_Salary": 500.0,
    "Num_Bank_Accounts": 8,
    "Num_Credit_Card": 6,
    "Interest_Rate": 28.0,
    "Num_of_Loan": 5,
    "Delay_from_due_date": 30,
    "Num_of_Delayed_Payment": 12,
    "Changed_Credit_Limit": 50000.0,
    "Num_Credit_Inquiries": 0,
    "Credit_Utilization_Ratio": 0.0,
    "Outstanding_Debt": 0.0,
    "Monthly_Balance": 0.0,
    "Age": 18,
    "Total_EMI_per_month": 0.0,
    "Type_of_Loan": "Personal Loan",
    "Payment_Behaviour": "Low_spent_Large_value_payments",
    "Amount_invested_monthly": 0.0,
    "Credit_Mix": "Bad",
    "Payment_of_Min_Amount": "No",
    "Credit_History_Age": "1 Year and 2 Months",
    "Occupation": "Unemployed"
  }
    res = requests.post(url, json=sample, headers=headers)
    assert res.status_code == 200
    assert res.json()["score"] in ["Good", "Standard", "Poor"]
