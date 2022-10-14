import os
from fastapi import FastAPI
from dotenv import load_dotenv
from influxdb_client import InfluxDBClient

load_dotenv()

ORG='Stock Sentiment Analyzer'
SENTIMENT_BUCKET='stock_sentiments'
TEXT_BUCKET='social_media_text'

app = FastAPI()
db_client = InfluxDBClient(
    url='http://localhost:8086',
    token=os.environ['INFLUX_API_TOKEN'],
    org=ORG
)
query_api = db_client.query_api()

def build_moving_avg_query(company:str, time_range:str) -> str:

    time_range_conversions = {
        'hour' : '-1h',
        'day': '-1d',
        'week': '-1w',
        'month': '-1mo'
    }

    return f'''from(bucket: "stock_sentiments")
  |> range(start: {time_range_conversions.get(time_range, '-1h')})
  |> filter(fn: (r) => r["_measurement"] == "stocks")
  |> filter(fn: (r) => r["_field"] == "compound")
  |> filter(fn: (r) => r["company"] == "{company}")
  |> timedMovingAverage(every: 5m, period: 10m )
  |> yield(name: "moving average")'''

@app.get('/moving_averages/{company}/{time_range}')
def get_moving_averages(company:str, time_range: str):

    result = query_api.query(
        org=ORG, 
        query=build_moving_avg_query(company, time_range)
    )

    moving_averages = []

    for table in result:
        for record in table.records:
            moving_averages.append((record.get_field(), record.get_value()))

    return {
        'success':True,
        'data': moving_averages,
    }