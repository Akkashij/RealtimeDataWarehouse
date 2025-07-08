import random
from datetime import datetime, timedelta
import pandas as pd
from airflow.sdk import DAG
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.providers.standard.operators.python import PythonOperator

start_date = datetime(2025, 6, 26)
default_args = {
    'owner': 'akkashij',
    'depends_on_past': False,
    'backfill': False
}

num_rows = 100
output_file = './customer_dim_large_data.csv'


# hàm tạo dữ liệu ngẫu nhiên cho customer data
def generate_random_data(row_num):
    customer_id = f'C{row_num:05d}'
    first_name = f'FirstName{row_num}'
    last_name = f'LastName{row_num}'
    email = f"customer{row_num}@example.com"
    phone_number = f"+84{random.randint(100000000, 999999999)}" 

    now = datetime.now()
    random_date = now - timedelta(days=random.randint(0, 3650)) # random date within the last 10 years
    registration_date_millis = int(random_date.timestamp() * 1000) 

    return customer_id, first_name, last_name, email, phone_number, registration_date_millis

# danh sách để lưu trữ dữ liệu
customer_ids = []
first_names = []
last_names = []
emails = []
phone_numbers = []
registration_dates = []

def generate_customer_dim_data():
    row_num = 1
    while row_num <= num_rows:
        customer_id, first_name, last_name, email, phone_number, registration_date_millis = generate_random_data(row_num)
        customer_ids.append(customer_id)
        first_names.append(first_name)
        last_names.append(last_name)
        emails.append(email)
        phone_numbers.append(phone_number)
        registration_dates.append(registration_date_millis) 
        row_num += 1

    # create DataFrame and save to CSV
    df = pd.DataFrame({
        "customer_id": customer_ids,
        "first_name": first_names,
        'last_name': last_names,
        "email": emails,
        "phone_number": phone_numbers,
        "registration_date": registration_dates
    })

    df.to_csv(output_file, index=False)

    print(f'CSV file {output_file} generated with {num_rows} rows.')


with DAG('customer_dim_generator',
         default_args=default_args,
         description='A DAG to generate customer dimension data',
         schedule=timedelta(days=1),
         start_date=start_date,
         tags=['dimension']) as dag:

    start = EmptyOperator(
        task_id = 'start_task'
    )

    generate_customer_dim_data = PythonOperator(
        task_id='generate_customer_dim_data',
        python_callable=generate_customer_dim_data
    )

    end = EmptyOperator(
        task_id='end_task'
    )

    start >> generate_customer_dim_data >> end