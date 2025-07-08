from datetime import datetime, timedelta

from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator


start_date = datetime(2025, 6, 26)
default_args = {
    'owner': 'akkashij',
    'depends_on_past': False,
    'backfill': False,
    'start_date': start_date
}

with DAG(
    dag_id='dimension_batch_ingestion',
    default_args=default_args,
    description='A DAG to ingest dimension data into Pinot',
    schedule='@daily',
    catchup=False
) as dag:
    ingest_account_dim = BashOperator(
        task_id='ingest_account_dim',
        # PINOT DATA INGESTION API - FILE UPLOAD
        # Source: Apache Pinot Controller UI (Swagger)
        # URL: http://localhost:9000/help#/Table/ingestFromFile
        bash_command= (
            'curl -X POST -F "file=@/opt/airflow/account_dim_large_data.csv" '
            '-H "Content-Type: multipart/form-data" '
            '"http://pinot-controller:9000/ingestFromFile?tableNameWithType=account_dim_OFFLINE&batchConfigMapStr=%7B%22inputFormat%22%3A%22csv%22%2C%22recordReader.prop.delimiter%22%3A%22%2C%22%7D"'

        )
    )

    ingest_customer_dim = BashOperator(
        task_id='ingest_customer_dim',
        # PINOT DATA INGESTION API - FILE UPLOAD
        # Source: Apache Pinot Controller UI (Swagger)
        # URL: http://localhost:9000/help#/Table/ingestFromFile
        bash_command= (
            'curl -X POST -F "file=@/opt/airflow/customer_dim_large_data.csv" '
            '-H "Content-Type: multipart/form-data" '
            '"http://pinot-controller:9000/ingestFromFile?tableNameWithType=customer_dim_OFFLINE&batchConfigMapStr=%7B%22inputFormat%22%3A%22csv%22%2C%22recordReader.prop.delimiter%22%3A%22%2C%22%7D"'

        )
    )

    ingest_branch_dim = BashOperator(
        task_id='ingest_branch_dim',
        # PINOT DATA INGESTION API - FILE UPLOAD
        # Source: Apache Pinot Controller UI (Swagger)
        # URL: http://localhost:9000/help#/Table/ingestFromFile
        bash_command= (
            'curl -X POST -F "file=@/opt/airflow/branch_dim_large_data.csv" '
            '-H "Content-Type: multipart/form-data" '
            '"http://pinot-controller:9000/ingestFromFile?tableNameWithType=branch_dim_OFFLINE&batchConfigMapStr=%7B%22inputFormat%22%3A%22csv%22%2C%22recordReader.prop.delimiter%22%3A%22%2C%22%7D"'

        )
    )

    #ingest_account_dim >> ingest_customer_dim >> ingest_branch_dim