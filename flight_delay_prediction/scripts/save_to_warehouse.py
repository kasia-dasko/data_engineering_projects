import pandas as pd
from airflow.providers.postgres.hooks.postgres import PostgresHook

def save_to_warehouse(ti):
    flights = ti.xcom_pull(key='flights', task_ids='fetch_raw_data')
    if not flights:
        raise ValueError("No data")
    
    processed_flights = []
    for flight in flights:
        processed_flights.append({
            'flight_date': flight.get('flight_date'),
            'airline_name': flight.get('airline', {}).get('name'),
            'dep_iata': flight.get('departure', {}).get('iata'),
            'min_delay_dep': flight.get('departure', {}).get('delay'),
        })
        
    df = pd.DataFrame(processed_flights)

    df['flight_date'] = pd.to_datetime(df['flight_date'], errors='coerce')
    df['min_delay_dep'] = pd.to_numeric(df['min_delay_dep'], errors='coerce').fillna(0).astype(int)
    df['airline_name'] = df['airline_name'].astype(str)
    df['dep_iata'] = df['dep_iata'].astype(str)
    
    hook = PostgresHook(postgres_conn_id='postgres_id')
    engine = hook.get_sqlalchemy_engine()

    df.to_sql('flights', engine, if_exists='append', index=False)

