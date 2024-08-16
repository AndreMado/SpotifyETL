from datetime import timedelta,datetime
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past':False,
    'start_date': datetime(2024,8,15),
    'email': ['andresxmaldonado@gmail.com'],
    'email_on_failure':True,
    'email_on_retry':True,
    'retries':1,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    'spotify_dag',
    default_args = default_args,
    description='Implemeting Airflow to my Spotify ETL process dag',
    schedule_interval= timedelta(minutes=3)
)

def testing_fuction():
    print("TESTINGGG")

run_etl = PythonOperator(
    task_id='whole_spotify_etl',
    python_callable=testing_fuction(),
    dag=dag
)

run_etl