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

dag = DAG(
    # ตั้งชื่อให้ตรงกับ file จะได้หาง่าย ชื่อซ้ำกันกับไฟล์อื่นมันไม่เจอนะ
    'tp_dag',
    default_args=default_args,
    description='My first Airflow DAG with an empty operator',
    # pipline จะรันหลังผ่านไปเท่าไร
    schedule_interval=timedelta(days=1),
    # เริ่มทำงานจริง +1 วัน คือ วันที่ 2 มกราคม
    start_date=datetime(2023, 1, 1),
    # รันเพื่อไป get ข้อมูลย้อนหลัง ถ้าจะใช้ต้องเป็น true
    catchup=False,
)

# เราเลือกใช้ได้ว่าจะใช้ EmptyOperator สำหรับค่าเปล่าไม่ต้องสร้าง def หรือใช้ PythonOperator สำหรับสร้าง def 
start_task = EmptyOperator(
    task_id='start_task',
    dag=dag,
)

intermediate_task = EmptyOperator(
    task_id='intermediate_task',
    dag=dag,
)

second_intermediate_task = EmptyOperator(
    task_id='second_intermediate_task',
    dag=dag,
)

send_line_message = EmptyOperator(
    task_id='send_line_message',
    dag=dag,
)

send_ms_team = EmptyOperator(
    task_id='send_ms_team',
    dag=dag,
)

send_email = EmptyOperator(
    task_id='send_email',
    dag=dag,
)

end_task = EmptyOperator(
    task_id='end_task',
    dag=dag,
)

start_task >> [intermediate_task, second_intermediate_task] >> end_task >> [send_line_message, send_ms_team]
second_intermediate_task >> [send_email, end_task] # หรือ second_intermediate_task >> send_email ก็ได้