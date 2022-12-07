import os
import re
import json
import torch
import numpy as np
from celery import Celery
from billiard.process import current_process
from celery.signals import worker_process_init
from dotenv import load_dotenv
from collections import Counter
from scipy.special import softmax
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from transformers import logging
from transformers import AutoTokenizer, AutoConfig
from transformers import AutoModelForSequenceClassification
from .preprocessing import (
    preprocess_text,
    sentiment_analysis_preprocess,
    text_analysis_preprocess,
)

MODEL = "cardiffnlp/twitter-roberta-base-sentiment-latest"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

stocks, stocks_reverse = {}, {}

with open("stocks.json") as stocks_fp:
    stocks = json.load(stocks_fp)["stocks"]
    stocks_reverse = {v: k for k, v in stocks.items()}

logging.set_verbosity_error()
load_dotenv()

app = Celery(
    "data_ingestion.sentiment_analysis.sentiment_analysis",
    broker=os.environ["BROKER_URL"],
)


@worker_process_init.connect
def init_worker(**kwargs):

    global tokenizer, config, model
    global db_client
    global name_regex, ticker_regex

    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    config = AutoConfig.from_pretrained(MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL).to(DEVICE)

    db_client = InfluxDBClient(
        url=os.environ["INFLUX_URL"],
        token=os.environ["INFLUX_API_TOKEN"],
        org=os.environ["ORG"],
    )

    name_regex = re.compile(f'({"|".join([name.lower() for name in stocks.keys()])})')
    ticker_regex = re.compile(
        f'({"|".join(["$"+ticker.lower() for ticker in stocks.values()])})'
    )

    os.environ["WORKER_NAME"] = current_process().name

    print(f'{os.environ["WORKER_NAME"]} initialized')


def recognize_company(text) -> str | None:

    text = text.lower()

    companies = name_regex.findall(text)
    tickers = ticker_regex.findall(text)

    companies += [stocks_reverse[ticker.upper()] for ticker in tickers]

    if len(companies) == 0:
        return None

    company, count = Counter(companies).most_common(1)[0]

    return stocks[company]


def apply_analysis(text: str) -> dict | None:

    result = {}
    company = recognize_company(text)
    text = preprocess_text(text)

    if company is None:
        return None

    encoded_input = tokenizer(
        text=sentiment_analysis_preprocess(text), return_tensors="pt"
    ).to(DEVICE)

    output = model(**encoded_input)
    scores = output[0][0].detach().cpu().numpy()
    scores = softmax(scores)

    ranking = np.argsort(scores)[::-1]

    for i in range(scores.shape[0]):
        l = config.id2label[ranking[i]]
        s = scores[ranking[i]]

        print(f"{i+1}) {l} {np.round(float(s), 4)}")

        result[l.lower()] = s

    result["compound"] = result["positive"] - result["negative"]
    result["company"] = company.upper()

    return result


@app.task(name="analyze_and_store")
def analyze_and_store(text: str) -> None:

    text = preprocess_text(text)
    result = apply_analysis(text)

    if not result is None:

        with db_client.write_api(write_options=SYNCHRONOUS) as write_api:

            point = (
                Point("stocks")
                .tag("company", result["company"])
                .field("compound", result["compound"])
                .field("negative", result["negative"])
                .field("positive", result["positive"])
                .field("neutral", result["neutral"])
            )

            write_api.write(
                bucket=os.environ["SENTIMENT_BUCKET"],
                org=os.environ["ORG"],
                record=point,
            )

            point = (
                Point("text")
                .tag("company", result["company"])
                .field("text", text_analysis_preprocess(text, result["company"]))
            )

            write_api.write(
                bucket=os.environ["TEXT_BUCKET"], org=os.environ["ORG"], record=point
            )
