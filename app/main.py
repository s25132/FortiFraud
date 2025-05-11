from fastapi import FastAPI, Depends, HTTPException
from app.utils.setup import get_predictor
from app.model.prediction_input import PredictionInput
from app.security.basic_security import check_auth
from app.validate.simple_validator import validate_non_empty_strings
import pandas as pd

app = FastAPI()
predictor = None

@app.on_event("startup")
def start_app():
    print("Startuję !")
    global predictor
    predictor = get_predictor()
    
@app.get("/")
def read_root():
    return {"message": "Welcome to FortiFraud app!"}

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
        