import os
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient

from .query_builder import build_moving_avg_query

load_dotenv()

db_client = InfluxDBClient(
    url='http://localhost:8086',
    token=os.environ['INFLUX_API_TOKEN'],
    org=os.environ['ORG']
)
query_api = db_client.query_api()

def get_moving_averages(company:str, time_range:str) -> list:

    result = query_api.query(
        org=os.environ['ORG'], 
        query=build_moving_avg_query(company, time_range)
    )

    moving_averages = []

    print(result)

    for table in result:
        for record in table.records:
            moving_averages.append(record.get_value())

    return moving_averages