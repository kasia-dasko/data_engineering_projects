from airflow.providers.postgres.hooks.postgres import PostgresHook
import pandas as pd

def select_columns(ti):
    hook = PostgresHook(postgres_conn_id='postgres_id')
    sql = """
    SELECT flight_date, airline_name, min_delay_dep, dep_iata
    FROM flights
    """
    df = hook.get_pandas_df(sql)
    df['is_delayed'] = df['min_delay_dep'].apply(lambda x: 1 if x and x> 15 else 0)
    ti.xcom_push(key='filtered_flights', value=df.to_json())

    df.to_sql('flights_filtered', con=engine, if_exists='append', index=False)    



