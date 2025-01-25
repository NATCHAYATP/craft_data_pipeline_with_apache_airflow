from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator

# default value
default_args = {
    'owner': 'airflow',
    # ต้องดู dag ก่อนหน้าหรือไม่
    'depends_on_past': False,
    # ส่ง mail มั้ยถ้าพัง
    'email_on_failure': False,
    'email_on_retry': False,
    # ถ้าเกิดพังจะ retry ให้รอบนึง
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# เรียกใช้ dag
dag = DAG(
    # ตั้งชื่อให้ตรงกับ file จะได้หาง่าย
    'first_dag',
    default_args=default_args,
    description='My first Airflow DAG with an empty operator',
    # pipline จะรันหลังผ่านไปเท่าไร
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 1, 1),
    # รันเพื่อไป get ข้อมูลย้อนหลัง ถ้าจะใช้ต้องเป็น true
    catchup=False,
)

def hello_world():
    print("hello world")

# สั่งให้มันไปรัน dag
start = EmptyOperator(
    task_id='start',
    dag=dag,
)

# เรียกใช้ func hello_word
hello_world = PythonOperator(
    task_id='hello-world',
    dag=dag,
    python_callable=hello_world
)

end = EmptyOperator(
    task_id='end',
    dag=dag,
)

# ลำดับการรัน
start >> hello_world >> end