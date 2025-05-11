import pandas as pd
import os
from fastapi import FastAPI, Depends, HTTPException
from app.predictor.predictor import get_predictor
from app.model.prediction_input import PredictionInput
from app.security.basic_security import check_auth
from app.validate.simple_validator import validate_non_empty_strings
from app.database.db_operation import insert_claim
from app.scheduler.metrics_scheduler import start_scheduler
from concurrent.futures import ThreadPoolExecutor

app = FastAPI()

max_workers = int(os.getenv("MAX_INSERT_CLAIM_WORKERS", "20"))
claim_executor = ThreadPoolExecutor(max_workers=max_workers)
predictor = None

@app.on_event("startup")
def start_app():
    print("Startuję !")
    global predictor
    predictor = get_predictor()

    if os.getenv("COLLECT_METRICS", "false").lower() == "true":
        start_scheduler()
    
@app.get("/")
def read_root():
    return {"message": "Welcome to FortiFraud app!"}

@app.post("/predict")
def predict(input_data: PredictionInput, _: str = Depends(check_auth)):
        if predictor is None:
            return {"status": "EMPTY PREDICTOR"}
    
        validate_non_empty_strings(input_data)

        input_df = pd.DataFrame([input_data.dict()])
        print(input_df)

        prediction = predictor.predict(input_df)
        probas = predictor.predict_proba(input_df)

        result = prediction.iloc[0]

        if os.getenv("COLLECT_CLAIMS", "false").lower() == "true":
             claim_executor.submit(insert_claim, input_data, result)

        message = 'NOT FRAUD' if result == 0 else 'POSSIBLE FRAUD'

        return {
            "status": "OK",
            "prediction": message,
            "probabilities": {k: float(v) for k, v in probas.iloc[0].items()}
        }


        