# craft_data_pipeline_with_apache_airflow

## create directory for airflow project
```
mkdir -p ./dags ./config ./logs ./plugins ./tests
```

# run airflow with docker compose 
- docker compose up --build

# learn stept
- tp_dag เพื่อสร้างการเรียกคำสั่ง 
- fetch_data.py เพื่อเอา data.zip ข้อมูลจาก kaggle มา
ปล. ต้องสร้าง directory data ด้วย จากนั้นใช้คำสั่ง python fetch_data.py มันจะไปอยู่ใน floder data ให่
- extract file
- google cloud แล้วสมัครโปรเจคใหม่ จากนั้นสร้าง buckets เลือก regious singapor -> continue รัวๆ
- จากนั้นไป IAM -> service accounts สร้างใหม่ซะ เลือก bigQuery -> bigQuery admin -> เลือก storage admin เข้าไปด้วย
- จากนั้นไปตรง tab เลือก role -> storage object creat, list, delete, get
- ไปที่ service account -> key -> add key -> json
- เอา json มาใส่ในนี้ แล้วเรียกใช้

- จากนั้นจะได้ directory ด้านใน airflow บนเว็บแล้ว ดูที่ buckets อ่ะ
- ไปต่อที่ขั้นตอนเอาข้อมูลลง big query ไปดูใน tpuploading/example_upload_local_file_to_bigquery.py เอานะ อธิบายละเอียด
- เขียน pipeline แต่เหมือนจะได้นิดเดียวง่ะ เราเขียนที่ dags/weather-api/greenery_etl.py เป็นการใช้ python operator
- เวลาลบ ลบ bigquery, ลบ IAM, ลบ service accou..
- โหลดข้อมูลจาก google cloud storage เอามา clean

ปล. gcp-credential.json เราเอามาจาก key แหละ ตอนสร้างอ่ะจะได้มาเราแค่เอามาเปลี่ยนชื่อให้สวยๆ

ปล. หยกมาช่วยแก้บัค ที่ตัง regious ผิด ให้ไปลบ bigquery greenery ทิ้งแล้วสร้างใหม่ สร้างยังไง ก็ไปที่ bigquery แหละ กดจุดสามจุดเลือก dataset 