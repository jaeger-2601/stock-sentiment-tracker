import json
from enum import Enum
from collections import Counter
from fastapi import status, APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache

from .. import flux_queries

import yahooquery as yq

router = APIRouter()

stocks = {}

with open("stocks.json") as stocks_fp:
    stocks = json.load(stocks_fp)["stocks"]


class TimeRange(str, Enum):
    day = "day"
    week = "week"
    month = "month"


class CacheTime(int, Enum):
    hour = 60 * 60
    day = 60 * 60 * 24
    month = 60 * 60 * 24 * 30


def valid_company(company: str):

    if not company in stocks.values():

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid company ticker"
        )

    return company


@router.get("/moving-averages/{company}/{time_range}")
async def get_moving_averages(
    time_range: TimeRange, company: str = Depends(valid_company)
):

    return {
        "data": flux_queries.get_moving_averages(company, time_range),
    }


@router.get("/word-counts/{company}/{time_range}")
async def get_word_count(time_range: TimeRange, company: str = Depends(valid_company)):

    text = flux_queries.get_social_media_text(company, time_range)
    text_blob = " ".join(text)
    words_counts = Counter(text_blob.split(" "))

    return {"data": words_counts.most_common(30)}


@router.get("/tickers-info/{time_range}")
async def get_ticker_info(time_range: TimeRange):

    overall_sentiment_scores = flux_queries.get_overall_sentiment_averages(time_range)

    data = [
        {
            "rank": i + 1,
            "company": s_data[0],
            "score": s_data[1],
        }
        for i, s_data in enumerate(overall_sentiment_scores)
    ]

    return {"data": data}


@router.get("/ticker-prices/{company}/{time_range}")
@cache(expire=CacheTime.hour.value)
async def get_ticker_prices(
    time_range: TimeRange, company: str = Depends(valid_company)
):

    period, interval = {
        "day": ["1d", "1h"],
        "week": ["7d", "1h"],
        "month": ["1mo", "1d"],
    }[time_range]

    ticker_history = yq.Ticker(company).history(period=period, interval=interval)

    return {"data": list(ticker_history["open"])}


@router.get("/company-summary/{company}")
@cache(expire=CacheTime.month.value)
async def get_company_summary(company: str = Depends(valid_company)):

    company_info = yq.Ticker(company)
    summary_profile = company_info.summary_profile[company]

    if company_info is None:
        return {"data": ""}
    else:
        return {"data": summary_profile["longBusinessSummary"]}


@router.get("/company-fundamentals/{company}")
@cache(expire=CacheTime.day.value)
async def get_company_fundamentals(company: str = Depends(valid_company)):

    company_info = yq.Ticker(company)
    financial_data = company_info.financial_data[company]
    key_stats = company_info.key_stats[company]
    summary_detail = company_info.summary_detail[company]

    if company_info is None:
        return {"data": ""}
    else:
        return {
            "data": {
                "basicStats": {
                    "revenue": financial_data["totalRevenue"],
                    "eps": key_stats["trailingEps"],
                    "totalDebt": financial_data["totalDebt"],
                    "trailingPE": summary_detail["trailingPE"],
                    "profitMarign": financial_data["profitMargins"],
                    "marketCap": summary_detail["marketCap"],
                },
                "historicGrowth": {
                    "revenueGrowth": financial_data["revenueGrowth"],
                    "epsGrowth": key_stats["forwardEps"],
                    "fiftyTwoWeekHigh": summary_detail["fiftyTwoWeekHigh"],
                    "fiftyTwoWeekLow": summary_detail["fiftyTwoWeekLow"],
                    "floatShares": key_stats["floatShares"],
                    "beta": key_stats["beta"],
                },
                "futureEstimates": {
                    "priceToBook": key_stats["priceToBook"],
                    "shortRatio": key_stats["shortRatio"],
                },
            }
        }


@router.get("/basic-info/{company}")
@cache(expire=CacheTime.month.value)
async def get_basic_info(company: str = Depends(valid_company)):

    company_info = yq.Ticker(company)

    name = company_info.price[company]["longName"]
    summary_profile = company_info.summary_profile[company]

    if company_info is None:
        return {"data": ""}
    else:
        return {
            "data": {
                "fullName": name,
                "industry": summary_profile["industry"],
                "country": summary_profile["country"],
                "fullTimeEmployees": summary_profile["fullTimeEmployees"],
            }
        }
