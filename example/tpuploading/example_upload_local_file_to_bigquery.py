from google.cloud import bigquery
import os
from google.oauth2 import service_account
import json

# อัปโหลดของจาก data ไปใน big query ของ web airflow
# ก่อนเริ่มไป bigQuery เพื่อสร้าง dataset ก่อน กดจุดสามจุด create data set -> regious singapor
# อาจใช้วิธีอื่นเช่น เชื่อ gg could กับ bigquery

keyfile = "gcp-credential.json"
local_file_path = "data/addresses.csv"
project_id = "valid-flow-448907-d4"
dataset_id = "greenary"
# มันคือชื่อ table ที่เราได้ตอนสร้างเสร็จง่ะ
table_id = "addresses"


def load_to_bigquery():
    service_account_info = json.load(open(keyfile))
    credentials = service_account.Credentials.from_service_account_info(service_account_info)
    client = bigquery.Client(
        project=project_id,
        credentials=credentials,
    )

    table_ref = client.dataset(dataset_id).table(table_id)
    # ด้านใน LoadJobConfig มี query ด้วย 
    # เพื่อเอาข้อมูลใน csv ลง bigquery นะ
    job_config = bigquery.LoadJobConfig(
        # autodetect เพิ่มมาเพราะไม่มี table ใน schema ไม่แนะนำให้ใช้ท่านี้ พี่มาท่านี้เพราะใน LoadJobConfig
        # ที่เรียกใช้ไม่ได้สร้าง table พี่เขา ขก สร้าง 555 แต่มีสักไฟล์ที่สร้าง table อยู่นะไปหาดูได้
        autodetect = True,
        source_format=bigquery.SourceFormat.CSV,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )

    # เอา file ขึ้นไปใน bigquery
    with open(local_file_path, "rb") as source_file:
        job = client.load_table_from_file(source_file, table_ref, job_config=job_config)

    job.result()  # Waits for the job to complete.

    print(f"Loaded {job.output_rows} rows into {dataset_id}:{table_id}.")

load_to_bigquery()
