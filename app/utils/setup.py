import os
import zipfile
from google.oauth2 import service_account
from googleapiclient.discovery import build
from autogluon.tabular import TabularPredictor
from tools import download_zip_file

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


def get_drive_service():

    credentials_path = os.getenv("GOOGLE_CREDENTIALS")
    if not credentials_path:
        raise ValueError("Missing GOOGLE_CREDENTIALS environment variable")
    
    SCOPES = ['https://www.googleapis.com/auth/drive']

    # Create credentials using the service account file
    credentials = service_account.Credentials.from_service_account_file(credentials_path, scopes=SCOPES)

    # Build the Google Drive service
    drive_service = build('drive', 'v3', credentials=credentials)
    return drive_service



