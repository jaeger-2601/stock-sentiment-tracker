import os

from dotenv import load_dotenv
from influxdb_client import InfluxDBClient

from .query_builder import (
    build_moving_avg_query,
    build_overall_sentiment_averages_query,
    build_social_media_text_query,
)

load_dotenv()

db_client = InfluxDBClient(
    url="http://localhost:8086",
    token=os.environ["INFLUX_API_TOKEN"],
    org=os.environ["ORG"],
)
query_api = db_client.query_api()


def get_moving_averages(company: str, time_range: str) -> list:

    result = query_api.query(
        org=os.environ["ORG"], query=build_moving_avg_query(company, time_range)
    )

    moving_averages = []

    for table in result:
        for record in table.records:
            moving_averages.append(record.get_value())

    return moving_averages


def get_social_media_text(company: str, time_range: str) -> list:

    result = query_api.query(
        org=os.environ["ORG"], query=build_social_media_text_query(company, time_range)
    )

    social_media_text = []

    for table in result:
        for record in table.records:

            val = record.get_value()
            if type(val) == str:
                social_media_text.append(record.get_value())

    return social_media_text


def get_overall_sentiment_averages(time_range: str) -> list:

    result = query_api.query(
        org=os.environ["ORG"], query=build_overall_sentiment_averages_query(time_range)
    )

    overall_sentiment_averages = []

    for table in result:
        for record in table.records:
            overall_sentiment_averages.append((record["company"], record.get_value()))

    return overall_sentiment_averages
