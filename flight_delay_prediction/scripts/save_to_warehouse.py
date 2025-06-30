import pandas as pd
from airflow.providers.postgres.hooks.postgres import PostgresHook

def save_to_warehouse(ti):
    flights = ti.xcom_pull(key='flights', task_ids='fetch_raw_data')
    if not flights:
        raise ValueError("No data")
    
     df = pd.DataFrame(flights)
     expected_columns = ['flight_date', 'airline_name', 'dep_iata', 'min_delay_dep']
     df = df[expected_columns]

     df['flight_date'] = pd.to_datetime(df['flight_date'], errors='coerce')
     df['min_delay_dep'] = pd.to_numeric(df['min_delay_dep'], errors='coerce').fillna(0).astype(int)
     df['airline_name'] = df['airline_name'].astype(str)
     df['dep_iata'] = df['dep_iata'].astype(str)
     
     hook = PostgresHook(postgres_conn_id='postgres_id')
     engine = hook.get_sqlalchemy_engine()

     df.to_sql('flights', engine, if_exists='append', index=False)

