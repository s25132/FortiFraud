import os
import zipfile
from autogluon.tabular import TabularPredictor
from tools import download_zip_file
from app.utils.setup import get_drive_service

def get_predictor():
   
    model_id = os.getenv("MODEL_ID")

    print(f"Model id: {model_id}")

    os.makedirs('model', exist_ok=True)

    zip_file = 'model/tabular_model.zip'

    unzipped_dir = 'unzipped_model'

    download_zip_file(suffix=model_id, folder_name='models', destination_path=zip_file, drive_service=get_drive_service())

    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(unzipped_dir)

    print(f"Model rozpakowany do: {unzipped_dir}")

    loaded_predictor = TabularPredictor.load(unzipped_dir)
    print("Model został wczytany z ZIP-a!")

    return loaded_predictor
