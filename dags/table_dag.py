import random
from datetime import datetime, timedelta

import pandas as pd
from airflow.sdk import DAG
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.providers.standard.operators.python import PythonOperator
from custom_operators.pinot_table_operator import PinotTableSubmitOperator

start_date = datetime(2025, 6, 26)
default_args = {
    'owner': 'akkashij',
    'depends_on_past': False,
    'backfill': False,
    'start_date': start_date
}

with DAG('table_dag',
         default_args=default_args,
         description='A DAG to submit all table in a folder to Apache Pinot',
         schedule=timedelta(days=1),
         start_date=start_date,
         tags=['table']) as dag:
    
    start = EmptyOperator(
        task_id='start_task'
    )

    submit_tables = PinotTableSubmitOperator(
        task_id='submit_tables',
        folder_path='/opt/airflow/dags/tables',
        pinot_url='http://pinot-controller:9000/tables'
    )

    end = EmptyOperator(
        task_id='end_task'
    )

    start >> submit_tables >> end

