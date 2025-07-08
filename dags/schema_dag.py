import random
from datetime import datetime, timedelta

import pandas as pd
from airflow.sdk import DAG
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.providers.standard.operators.python import PythonOperator
from custom_operators.pinot_schema_operator import PinotSchemaSubmitOperator

start_date = datetime(2025, 6, 26)
default_args = {
    'owner': 'akkashij',
    'depends_on_past': False,
    'backfill': False,
    'start_date': start_date
}

with DAG('schema_dag',
         default_args=default_args,
         description='A DAG to submit all schema in a folder to Apache Pinot',
         schedule=timedelta(days=1),
         start_date=start_date,
         tags=['schema']) as dag:
    
    start = EmptyOperator(
        task_id='start_task'
    )

    submit_schema = PinotSchemaSubmitOperator(
        task_id='submit_schemas',
        folder_path='/opt/airflow/dags/schemas',
        pinot_url='http://pinot-controller:9000/schemas'
    )

    end = EmptyOperator(
        task_id='end_task'
    )

    start >> submit_schema >> end

