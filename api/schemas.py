
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
    Age: float


class PredictionOutput(BaseModel):
    score: str
