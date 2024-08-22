from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

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

run_etl = BashOperator(
    task_id='whole_spotify_etl',
    bash_command='python /home/app/main.py',
    dag=dag,
)

run_etl