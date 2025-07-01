from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta
import sys
sys.path.insert(0, '/opt/airflow/scripts')

from fetch_raw_data import fetch_raw_data
from save_to_warehouse import save_to_warehouse
from select_columns import select_columns

dag_1_args = {
    'owner': 'kasia',                
    'depends_on_past': False,        
    'start_date': datetime(2025, 7, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),  #
}

with DAG(
    dag_id='flight_data_pipeline',      
    default_args=dag_1_args ,
    schedule_interval='@daily',
    catchup=False,
) as dag:

    create_table = PostgresOperator(
        task_id='create_table_raw_data',
        postgres_conn_id='postgres_id',
        sql='/opt/airflow/db/create_table_raw_data.sql'
    )

    task_fetch = PythonOperator(
        task_id='fetch_raw_data',         
        python_callable=fetch_raw_data,   
        provide_context=True              
    )

    task_warehouse = PythonOperator(
        task_id='save_to_warehouse',
        python_callable=save_to_warehouse,
        provide_context=True
    )

    task_new_column = PythonOperator(
        task_id='select_columns',
        python_callable=select_columns,
        provide_context=True
    )

    create_table >> task_fetch >> task_warehouse >> task_new_column

