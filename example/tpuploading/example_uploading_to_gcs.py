import json
import os
import sys

from google.api_core import exceptions
from google.cloud import storage
from google.oauth2 import service_account

# เชื่อ google cloud กับ project ของเรา
def upload_to_gcs():
    # """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    bucket_name = "test_upload_gcs_tp_01"
    # The path to your file to upload
    source_file_name = "data/addresses.csv"
    # The ID of your GCS object มันจะเอาอันนี้เข้าไปสร้างใน test_upload_gcs_tp_01 ใน airflow web อ่ะ
    destination_blob_name = "greenery-data/addresses.csv"

    keyfile = "gcp-credential.json"
    service_account_info = json.load(open(keyfile))
    credentials = service_account.Credentials.from_service_account_info(service_account_info)
    #เอามาจากชื่อด้านบนที่เป็นปุ่มอ่ะ airflow-tutorial กดเข้าไปมันจะมี id
    project_id = "valid-flow-448907-d4"

    storage_client = storage.Client(
        project=project_id,
        credentials=credentials,
    )
    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        f"File {source_file_name} uploaded to {destination_blob_name}."
    )
upload_to_gcs()


# if __name__ == "__main__":
#     upload_blob(
#         bucket_name=sys.argv[1],
#         source_file_name=sys.argv[2],
#         destination_blob_name=sys.argv[3],
#     )