import os
from dotenv import load_dotenv

load_dotenv()

time_range_conversions = {
    'hour' : '-1h',
    'day': '-1d',
    'week': '-1w',
    'month': '-1mo'
}


def build_moving_avg_query(company:str, time_range:str) -> str:

    return f'''
    from(bucket: "{os.environ['SENTIMENT_BUCKET']}")
        |> range(start: {time_range_conversions.get(time_range, '-1h')})
        |> filter(fn: (r) => r["_measurement"] == "stocks")
        |> filter(fn: (r) => r["_field"] == "compound")
        |> filter(fn: (r) => r["company"] == "{company}")
        |> timedMovingAverage(every: 5m, period: 10m )
        |> yield(name: "moving average")
    '''

def build_social_media_text_query(company:str, time_range:str) -> str:

    return f'''
     from(bucket: "{os.environ['TEXT_BUCKET']}")
        |> range(start: {time_range_conversions.get(time_range, '-1h')})
        |> filter(fn: (r) => r["_measurement"] == "text")
        |> filter(fn: (r) => r["_field"] == "text")
        |> filter(fn: (r) => r["company"] == "{company}")
        |> yield(name: "social media text")
    '''