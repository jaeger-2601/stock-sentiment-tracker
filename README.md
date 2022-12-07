# Stock Sentiment Tracker

Stock Sentiment Tracker is an innovative platform for monitoring the current market sentiments regarding the top twenty five stocks in the Dow Jones Industrial Average (DJIA) index. This is done through real time sentiment analysis of textual information from social media sites like Twitter and Reddit.

## Rationale behind the project
Stock Market sentiment refers to the overall attitude of investors towards a particular security or financial market. It is the feeling of a market or its crowd psychology, as revealed through the activity and price movement of the market. Stock prices are hard  to predict because of their highly volatile nature which depends on diverse political and economic factors, investor sentiment, and many other factors. Market sentiment is a qualitative measure of the attitude and mood of investors to financial markets in general, and specific sectors or assets in particular. Positive and negative sentiment drive price action, and also create trading and investment opportunities for active traders and long-term investors.

Analyzing stock prices based on either historical data or textual information alone has proven to be insufficient. Sentiments have turned out to be a significant influence on the movement of the stock market and social media as a powerful resource for market predictions.

Sentiment analysis is an interesting branch of Natural Language Processing (NLP), which is used to rate the language used in a body of text at various levels using algorithms, deep learning etc, but the accuracy obtained is limited. The aim of this project is to build a stock sentiment tracking platform that utilizes textual informatiom from multiple sources (i.e Twitter and Reddit) to analyze sentiment regarding the top twenty five DJIA stocks. 

## Novelties of the project

- **Live insights into the sentiment of the stock market:** The sentiment of the stock market can change rapidly in relation with breaking news and information. With sentiment analysis on textual information from social media, one can quickly visualize the changing sentiments of the stock market and make appropriate portfolio decisons. 

- **Multiple Streams of Data:** The platform processes mutiple streams of data from social media sites like Twitter and Reddit in real time to improve the accuracy of sentiment analysis.

- **Capturing Key markers using NLP:** NLP techniques like Tag Clouds/Word Clouds can provide deeper insights into the sentiment surrounding a stock. 

## Architecture

![Main Architecture](images/main-architecture.png)
The proposed system uses real time streaming data from two data sources (Twitter and Reddit) for sentiment analysis.
- The data is first pre-processed and sent to a sentiment analysis module through a task queue.
- The sentiment analysis module applies NLP and sentiment analysis to extract information from the data and stores it in the Influx time-series database.
- This database can then be used by the API to fetch relevant data from the database to send to the front end.
- The frontend then visualizes the data in various ways to provide knowledge to the user.

The system can be divided logically into two modules: Data Ingestion and Data Representation.

### Data Ingestion Architecture
![Data Ingestion Architecture](images/data-ingestion-architecture.png)
The data ingestion module is composed of Aggregators, Message Queue, Distributed Task Manager, Sentiment Analysis Workers.
- **Aggregators**: Aggregators are components that aggregate data from their corresponding sources i.e Twitter and Reddit. This data is then sent to sentiment analysis workers using a message queue.
- **Message Queue**: RabbitMQ is used by Celery to facilitate communication between the aggregators and sentiment analysis workers
- **Distributed Task Manager**: Celery acts as a distributed task manager and manages the sentiment analysis workers and communication with them. Workers are spun up and spun down depending on the quantity of data received from aggregators.
- **Sentiment Analysis Workers**: Sentiment analysis workers are components which do preprocessing and sentiment analysis on text received from aggregators.

### Data Representation Architecture
![Data Representation Architecture](images/data-representation-architecture.png)
The data representation module is composed of API, Frontend UI, Stock data API.
- **API**: The API uses FastAPI for routing, validation etc .and Flux queries for querying and analyzing the data.
- **Frontend UI**: The frontend UI utilizes the axios library to communicate with the backend api and stock data api. React is used to declaratively build the UI while Chart.js performs visualizations to present the data in a meaningful manner
- **Stock data API**: Yahoo! Finance stock data api is queried to show the price information about various stocks.

### Setup
This project requires docker and docker compose to run.

1. Docker images must be first built using the following command:
```bash
docker compose build
```

2. Start InfluxDB alone using the following command:
```bash
docker compose up influx_db
```

3. Create an account and organization by using the dashboard at http://localhost:8086. 

4. Create two buckets in InfluxDB.
    - One to store sentiment information.
    - Another one to store textual information.

5. Create an `environments` directory to store all environment variables and create the following .env files
    - `.env.influx_db`
    - `.env.rabbit_mq`
    - `.env.reddit`
    - `.env.twitter`
    - `.env.redis`


6. Set the following environment variables with appropriate values in the environment files as listed below:
    - `.env.influx_db`
        - `INFLUX_URL`: URL to InfluxDB
        - `INFLUX_API_TOKEN`: InfluxDB API token
        - `ORG`: InfluxDB organization name
        - `SENTIMENT_BUCKET`: Sentiment data bucket name
        - `TEXT_BUCKET`: Textual data bucket name
    - `.env.reddit`
        - `CLIENT_ID`: Reddit client id
        - `CLIENT_SECRET`: Reddit client secret
    - `.env.twitter`
        - `API_KEY:` Twitter API key
        - `API_KEY_SECRET`: Twitter API key secret
        - `BEARER_TOKEN`: Twitter bearer token
    - `.env.redis`
        - `REDIS_URL`: URL to Redis
    - `.env.rabbit_mq`
        - `BROKER_URL`: URL to RabbitMQ broker

### Execution
The docker compose file has three profiles:
1. **Data Ingestion**: Run only services required for data ingestion i.e InfluxDB, RabbitMQ, Aggregators, Flower and Celery
```bash
docker compose --profile data_ingestion
```
2. **Data Representation**: Run only services required for data representation i.e InfluxDB, Redis, API and UI
```bash
docker compose --profile data_representation up
```
3. **All**: Run all services
```bash
docker compose --profile all up
```