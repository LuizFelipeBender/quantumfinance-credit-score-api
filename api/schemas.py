from pydantic import BaseModel

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
