from pydantic import BaseModel

class PredictionInput(BaseModel):
    Month: str
    WeekOfMonth: int
    Make: str
    AccidentArea: str
    MonthClaimed: str
    MaritalStatus: str
    Fault: str
    PolicyType: str
    VehicleCategory: str
    Deductible: int
    PoliceReportFiled: bool
    AgentType: str
    AddressChange_Claim: str
    Year: int
    BasePolicy: str