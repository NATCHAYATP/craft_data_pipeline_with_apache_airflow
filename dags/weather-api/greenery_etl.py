from datetime import datetime
import json
from airflow.decorators import dag, task
from google.oauth2 import service_account
from google.cloud import storage, bigquery

# ยังไม่ถูกตอนทำน่าจะลืมเลือก singapor อ่ะ
@dag(schedule_interval=None, start_date=datetime(2024, 1, 24), catchup=False)
def greenery_etl():
    bucket_name = "test_upload_gcs_tp_01"
    # The path to your file to upload
    # อันนี้เราไม่ได้รันบน local มันเลยมีตัวที่ docker-compose.yaml มัน mute ไว้เลยต้องใส่ path แบบนี้
    source_file_name = "/opt/airflow/data/addresses.csv"
    # The ID of your GCS object มันจะเอาอันนี้เข้าไปสร้างใน test_upload_gcs_tp_01 ใน airflow web อ่ะ
    destination_blob_name = "greenery-data/addresses.csv"

    # อันนี้เราไม่ได้รันบน local มันเลยมีตัวที่ docker-compose.yaml มัน mute ไว้เลยต้องใส่ path แบบนี้
    keyfile = "/opt/airflow/gcp-credential.json"
    #เอามาจากชื่อด้านบนที่เป็นปุ่มอ่ะ airflow-tutorial กดเข้าไปมันจะมี id
    project_id = "valid-flow-448907-d4"

    service_account_info = json.load(open(keyfile))
    credentials = service_account.Credentials.from_service_account_info(service_account_info)

    @task()
    def load_to_gcs():
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

    @task()
    def clean_greenery():
        pass

    @task()
    def load_from_gcs_to_bigquery():
        # เอามาจาก bigquery กดไปตรง detail
        dataset_id = "greenary"
        table_id = "addresses"

        client = bigquery.Client(project=project_id, credentials=credentials)

        table_ref = client.dataset(dataset_id).table(table_id)
        job_config = bigquery.LoadJobConfig(
            autodetect = True,
            source_format=bigquery.SourceFormat.CSV,
            write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        )

        source_file_name = "greenery-data/addresses.csv"
        uri = f"gs://{bucket_name}/{source_file_name}"

        load_job = client.load_table_from_uri(
            uri,
            table_ref,
            job_config=job_config,
        )

        load_job.result()  # Waits for the job to complete.

        print(f"Loaded {load_job.output_rows} rows into {dataset_id}:{table_id}.")

    load_to_gcs() >> clean_greenery() >> load_from_gcs_to_bigquery()

greenery_etl()