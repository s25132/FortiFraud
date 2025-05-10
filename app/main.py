from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.utils.setup import get_predictor
from app.model.prediction_input import PredictionInput
import os
import secrets
import pandas as pd

app = FastAPI()
security = HTTPBasic()
predictor = None

@app.on_event("startup")
def start_app():
    print("Startuję !")
    global predictor
    predictor = get_predictor()
    
@app.get("/")
def read_root():
    return {"message": "Welcome to FortiFraud app!"}


def check_auth(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, os.getenv("AUTH_LOGIN"))
    correct_password = secrets.compare_digest(credentials.password, os.getenv("AUTH_PASSWORD"))
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Basic"},
        )

def validate_non_empty_strings(data):
    for field_name, value in data:
        if isinstance(value, str) and value.strip() == "":
            raise HTTPException(
                status_code=400,
                detail=f"Pole '{field_name}' nie może być puste."
            )
        
@app.post("/predict")
def predict(input_data: PredictionInput, _: str = Depends(check_auth)):
    if predictor is None:
        return {"status": "EMPTY PREDICTOR"}
    
    
    validate_non_empty_strings(input_data)

    try:
        input_df = pd.DataFrame([input_data.model_dump()])
        print(input_df)

        prediction = predictor.predict(input_df)
        probas = predictor.predict_proba(input_df)

        result = prediction.iloc[0]
        message = 'NOT FRAUD' if result == 0 else 'POSSIBLE FRAUD'

        return {
            "status": "OK",
            "prediction": message,
            "probabilities": {k: float(v) for k, v in probas.iloc[0].items()}
        }

    except Exception as e:
        # Zwróć błąd 500 z komunikatem
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
        