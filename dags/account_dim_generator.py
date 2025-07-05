import random
# from airflow.operators.empty import EmptyOperator
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.providers.standard.operators.python import PythonOperator
# from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
from airflow.sdk import DAG

start_date = datetime(2025, 6, 26)
defaultargs = {
    'owner':'akkashij',
    'depends_on_past': False,
    'backfill': False
}

num_rows = 50
output_file = './account_dim_large_data.csv'

account_ids = []
account_types = []
statuses = []
customer_ids = []
balances = []
opening_dates = []

def generate_random_data(row_num):
    account_id = f'A{row_num:05d}'
    account_type = random.choice(['SAVINGS', 'CHECKING'])
    status = random.choice(['ACTIVE', 'INACTIVE'])
    customer_id = f'C{random.randint(1, 1000):05d}'
    balance = round(random.uniform(100.00, 10000.00), 2)

    now = datetime.now()
    random_date = now - timedelta(days=random.randint(0, 365))
    opening_date_millis = int(random_date.timestamp() * 1000) 

    return account_id, account_type, status, customer_id, balance, opening_date_millis

def generate_account_dim_data():
    row_num = 1
    while row_num <= num_rows:
        account_id, account_type, status, customer_id, balance, opening_date_millis = generate_random_data(row_num)
        account_ids.append(account_id)
        account_types.append(account_type)
        statuses.append(status)
        customer_ids.append(customer_id)
        balances.append(balance)
        opening_dates.append(opening_date_millis)
        row_num += 1

    df = pd.DataFrame({
        'account_id': account_ids,
        'account_type': account_types,
        'status': statuses,
        'customer_id': customer_ids,
        'balance': balances,
        'opening_date': opening_dates
    })

    df.to_csv(output_file, index=False)

    print(f'CSV file {output_file} generated with {num_rows} rows.')

with DAG(
    dag_id='account_dim_generator',
    default_args=defaultargs,
    description='Generate account dimension data',
    schedule=timedelta(days=1),
    start_date=start_date,
    tags=['schema'] 
) as dag:

    start = EmptyOperator(
        task_id='start_task'
    )

    generate_account_dimension_data = PythonOperator(
        task_id='generate_account_dim_data',
        python_callable=generate_account_dim_data
    )

    end = EmptyOperator(
        task_id='end_task'
    )

    start >> generate_account_dimension_data >> end

