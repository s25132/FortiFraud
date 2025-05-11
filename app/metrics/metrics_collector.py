import os
import pandas as pd
import wandb
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
from tools import download_file
from app.utils.setup import get_drive_service
from app.database.db_operation import collect_claims


def get_reference_data():
    os.makedirs('tmp', exist_ok=True)

    file_id = os.getenv("TEST_DATA_ID", None)

    print(f"Przetwarzam plik o ID: {file_id}")
    drive_service = get_drive_service()

    X_test = download_file(suffix=file_id, folder_name='X_test_data', destination_path='tmp/X_test_data.csv', drive_service=drive_service)
    y_test = download_file(suffix=file_id, folder_name='y_test_data', destination_path='tmp/y_test_data.csv', drive_service=drive_service)

    test_data = pd.concat([X_test, y_test], axis=1)
    
    print(test_data.head())

    return test_data

def get_new_data_from_archive():
    return collect_claims()

def collect_metrics():
    reference_data = get_reference_data()
    new_data = get_new_data_from_archive()

    new_data = new_data.rename(columns={'Prediction': 'FraudFound_P'})

    if reference_data is None or new_data is None:
        raise ValueError("Dane referencyjne lub nowe nie zostały poprawnie załadowane!")

    if set(reference_data.columns) != set(new_data.columns):
        raise ValueError("Kolumny muszą być takie same! Różnice: "
                     f"{set(reference_data.columns) ^ set(new_data.columns)}")

    # Logowanie do W&B
    wandb.init(project="fraud_oracle")

    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=reference_data, current_data=new_data)

    report.save_html("data_drift_report.html")
    wandb.save("data_drift_report.html")
    wandb.log({"DataDrift Report": wandb.Html("data_drift_report.html")})

    wandb.finish()
    print("DataDrift Report został przesłany do wandb.")