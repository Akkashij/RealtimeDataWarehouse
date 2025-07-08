from airflow.sdk import DAG
from airflow.providers.standard.operators.empty import EmptyOperator
from custom_operators.kafka_operator import KafkaProduceOperator
from datetime import datetime, timedelta

start_date = datetime(2025, 6, 26)
default_args = {
    'owner': 'akkashij',
    'depends_on_past': False,
    'backfill': False,
    'start_date': start_date
}

with DAG(
    dag_id='transaction_facts_generator',
    default_args=default_args,
    description='Transaction fact data generator into kafka',
    schedule=timedelta(days=1),
    tags=['face_data']
) as dag:

    start = EmptyOperator(task_id='start_task')

    generate_txn_data = KafkaProduceOperator(
        task_id='generate_txn_fact_data',
        kafka_broker='kafka_broker:9092',
        kafka_topic='transaction_facts',
        num_records=100
    )

    end = EmptyOperator(task_id='end_task')

    start >> generate_txn_data >> end