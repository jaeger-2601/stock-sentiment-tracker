import os
from dotenv import load_dotenv

load_dotenv()

time_range_conversions = {
    
    'day':['-1d', '1h'],
    'week':['-1wk', '2h'],
    'month':['-1mo', '1d']
}


def build_moving_avg_query(company:str, time_range:str) -> str:

    return f'''
        from(bucket: "{os.environ['SENTIMENT_BUCKET']}")
            |> range(start: {time_range_conversions[time_range][0]})
            |> filter(fn: (r) => r["_measurement"] == "stocks")
            |> filter(fn: (r) => r["_field"] == "compound")
            |> filter(fn: (r) => r["company"] == "{company}")
            |> timedMovingAverage(every: {time_range_conversions[time_range][1]}, period: 10m )
            |> yield(name: "moving average")
    '''

def build_social_media_text_query(company:str, time_range:str) -> str:

    return f'''
        from(bucket: "{os.environ['TEXT_BUCKET']}")
            |> range(start: {time_range_conversions[time_range][0]})
            |> filter(fn: (r) => r["_measurement"] == "text")
            |> filter(fn: (r) => r["_field"] == "text")
            |> filter(fn: (r) => r["company"] == "{company}")
            |> yield(name: "social media text")
    '''

def build_overall_sentiment_averages_query(time_range:str) -> str:

    return f'''
        from(bucket: "{os.environ['SENTIMENT_BUCKET']}")
            |> range(start: {time_range_conversions[time_range][0]})
            |> filter(fn: (r) => r["_measurement"] == "stocks")
            |> filter(fn: (r) => r["_field"] == "compound")
            |> group(columns: ["company"])
            |> mean(column: "_value")
            |> group()
            |> sort(columns: ["_value"], desc: true)
    '''