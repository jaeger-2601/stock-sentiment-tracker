from enum import Enum
from collections import Counter
from fastapi import status, APIRouter, Depends, HTTPException
from data_ingestion.stocks import djia_stocks

from app import flux_queries

import yfinance as yf

router = APIRouter()

class TimeRange(str, Enum):
    day='day'
    week='week'
    month='month'


def valid_company(company:str):

    if not company in djia_stocks.values():

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail='Invalid company ticker'
        )

    return company

@router.get('/moving-averages/{company}/{time_range}')
def get_moving_averages(time_range:TimeRange, company:str = Depends(valid_company)):

    return {
        'data': flux_queries.get_moving_averages(company, time_range),
    }

@router.get('/word-counts/{company}/{time_range}')
def get_word_count(time_range:TimeRange, company:str = Depends(valid_company)):

    text = flux_queries.get_social_media_text(company, time_range)
    text_blob = ' '.join(text)
    words_counts = Counter(text_blob.split(' '))

    return {
        'data': words_counts.most_common(30)
    }

@router.get('/tickers-info/{time_range}')
def get_ticker_info(time_range:TimeRange):

    overall_sentiment_scores = flux_queries.get_overall_sentiment_averages(time_range)

    data = [ 
        {
            'rank': i+1, 
            'company': s_data[0], 
            'score': s_data[1], 
        } 
        for i, s_data in enumerate(overall_sentiment_scores)
    ]

    return {
        'data': data
    }

@router.get('/ticker-prices/{company}/{time_range}')
def get_ticker_prices(time_range:TimeRange, company:str = Depends(valid_company)):

    period, interval = {
        'day':['1d', '1h'],
        'week':['1wk', '2h'],
        'month':['1mo', '1d']
    }[time_range]

    ticker_history = yf.Ticker(company).history(period=period, interval=interval)

    return {
        'data': list(ticker_history['Open'])
    }
