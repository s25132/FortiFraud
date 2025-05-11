import sqlitecloud
import os
import pandas as pd
from app.model.prediction_input import PredictionInput

def insert_claim(claim : PredictionInput, prediction : int):

    databse_key = os.getenv("SQL_CONNESCTION")

    if not databse_key:
        raise ValueError("Missing SQL_CONNESCTION environment variable")

    print("Inserting claim...")

    data = claim.dict()
    values = (
        data['Month'],
        int(data['WeekOfMonth']),
        data['Make'],
        data['AccidentArea'],
        data['MonthClaimed'],
        data['MaritalStatus'],
        data['Fault'],
        data['PolicyType'],
        data['VehicleCategory'],
        int(data['Deductible']),
        bool(data['PoliceReportFiled']),
        data['AgentType'],
        data['AddressChange_Claim'],
        int(data['Year']),
        data['BasePolicy'],
        int(prediction)
    )

    conn = sqlitecloud.connect(databse_key)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO archived_clames (
            Month, WeekOfMonth, Make, AccidentArea, MonthClaimed,
            MaritalStatus, Fault, PolicyType, VehicleCategory,
            Deductible, PoliceReportFiled, AgentType, AddressChange_Claim,
            Year, BasePolicy, Prediction
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    ''', values)

    conn.commit()
    conn.close()
  
def collect_claims() -> pd.DataFrame:

    databse_key = os.getenv("SQL_CONNESCTION")

    if not databse_key:
        raise ValueError("Missing SQL_CONNESCTION environment variable")
    
    limit = int(os.getenv("CLAIMS_LIMIT", "3000"))
    
    conn = sqlitecloud.connect(databse_key)
    cursor = conn.cursor()

    cursor.execute(f'''
        SELECT
            Month,
            WeekOfMonth,
            Make,
            AccidentArea,
            MonthClaimed,
            MaritalStatus,
            Fault,
            PolicyType,
            VehicleCategory,
            Deductible,
            PoliceReportFiled,
            AgentType,
            AddressChange_Claim,
            Year,
            BasePolicy,
            Prediction
        FROM archived_clames
        ORDER BY Created DESC
        LIMIT ?
    ''', (limit,)) 

    rows = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    conn.close()

    data = pd.DataFrame(rows, columns=columns)
    print(data.head())

    return data