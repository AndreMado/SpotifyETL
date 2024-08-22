from airflow import DAG
import sys
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from spotify_etl import run_spotify_etl

sys.path.append('/opt/airflow/plugins')

default_args = {
    'owner': 'airflow',
    'depends_on_past':False,
    'start_date': datetime(2024,8,21),
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
    schedule_interval= timedelta(minutes=5)
)

def just_a_function():
    print("HELLO")

run_etl = PythonOperator(
    task_id='whole_spotify_etl',
    python_callable=run_spotify_etl,
    dag=dag,
)

run_etl