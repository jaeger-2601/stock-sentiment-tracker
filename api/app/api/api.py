from enum import Enum
from fastapi import APIRouter

from app import flux_queries

router = APIRouter()

class TimeRange(str, Enum):
    hour='hour'
    day='day'
    week='week'
    month='month'


@router.get('/moving_averages/{company}/{time_range}')
def get_moving_averages(company:str, time_range: TimeRange):


    return {
        'success':True,
        'data': flux_queries.get_moving_averages(company, time_range),
    }