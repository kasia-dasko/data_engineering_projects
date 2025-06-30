import pandas as pd
from airflow.providers.postgres.hooks.postgres import PostgresHook

def save_to_warehouse(ti):
    flights = ti.xcom_pull(key='flights', task_ids='fetch_raw_data')
    if not flights:
        raise ValueError("No data")
    
     df = pd.DataFrame(flights)
     hook = PostgresHook(postgres_conn_id='postgres_id')
     engine = hook.get_sqlalchemy_engine()

     df.to_sql('flights', engine, if_exists='replace', index=False)

