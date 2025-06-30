import requests
import pandas as pd 

API_KEY = "c284b8b093d3e8234447863f11987d0b"

def fetch_raw_data(ti):
    url = f"https://api.aviationstack.com/v1/flights?access_key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        flights = data.get('data', [])
        ti.xcom_push(key='flights', value=flights)
    else:
        raise Exception(f"API request failed, status {response.status_code}")



     







