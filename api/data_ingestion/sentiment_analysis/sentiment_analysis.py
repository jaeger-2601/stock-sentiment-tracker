import os
from celery import Celery
from dotenv import load_dotenv
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client import InfluxDBClient, Point
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from data_ingestion.stocks import djia_stocks
from data_ingestion.preprocessing import remove_uneccesary_words

'''
TODO : Use roberta model instead of vader sentiment

from transformers import AutoModelForSequenceClassification
from transformers import TFAutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig

MODEL = 'cardiffnlp/twitter-roberta-base-sentiment-latest'

tokenizer = AutoTokenizer.from_pretrained(MODEL)
config = AutoConfig.from_pretrained(MODEL)
# PT
model = AutoModelForSequenceClassification.from_pretrained(MODEL)

@app.task
def apply_analysis(text:str):

    encoded_input = tokenizer(text, return_tensors='pt')
    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)

    ranking = np.argsort(scores)
    ranking = ranking[::-1]
    for i in range(scores.shape[0]):
        l = config.id2label[ranking[i]]
        s = scores[ranking[i]]

        with open('p.txt', 'w') as fp:
            fp.write(f"{i+1}) {l} {np.round(float(s), 4)}\n")

        print(f"{i+1}) {l} {np.round(float(s), 4)}")
'''

load_dotenv()

app = Celery('sentiment_analysis', broker='pyamqp://guest@localhost//')
db_client = InfluxDBClient(
    url='http://localhost:8086',
    token=os.environ['INFLUX_API_TOKEN'],
    org=os.environ['ORG']
)
analyzer = SentimentIntensityAnalyzer()

def recognize_company(text) -> str | None:

    for ticker, name in djia_stocks.items():
        
        if f'cashtag_{ticker[1:]}' in text or name in text:
            return name


@app.task
def analyze_and_store(text:str) -> None:

    result = analyzer.polarity_scores(text)
    company = recognize_company(text)


    if not company is None:

        with db_client.write_api(write_options=SYNCHRONOUS) as write_api:

            point = Point('stocks') \
                .tag('company', company) \
                .field('compound', result['compound']) \
                .field('negative', result['neg']) \
                .field('positive', result['pos']) \
                .field('neutral', result['neu'])
            
            write_api.write(
                bucket=os.environ['SENTIMENT_BUCKET']
                org=os.os.environ['ORG'], 
                record=point
            )

            point = Point('text') \
                .tag('company', company) \
                .field('text', remove_uneccesary_words(text, company))

            write_api.write(
                bucket=os.environ['TEXT_BUCKET'], 
                org=os.environ['ORG'], 
                record=point
            )


