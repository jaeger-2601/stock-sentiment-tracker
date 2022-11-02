from enum import Enum
from collections import Counter
from data_ingestion.preprocessing import text_analysis_preprocess
from fastapi import status, APIRouter, Depends, HTTPException
from data_ingestion.stocks import djia_stocks

from app import flux_queries

router = APIRouter()

class TimeRange(str, Enum):
    hour='hour'
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
