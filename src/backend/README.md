# Stock Sentiment Tracker Backend

### Setup
The backend uses poetry for dependecy management. To install all dependencies, run:
```bash
poetry install --with dev
```
If the machine has a GPU that has CUDA cores and supports CUDA 11, then run:
```bash
poetry download-pytorch-cuda11
```
else, run:
```bash
poetry download-pytorch-cpu
```

[*Optional*] Install InfluxDB and RabbitMQ with official installers from their respective sites.
- [InfluxDB](https://www.influxdata.com/get-influxdb/)
- [RabbitMQ](https://www.rabbitmq.com/download.html)

Create two buckets in InfluxDB.
- One to store sentiment information.
- Another one to store textual information.

Set the following environment variables with appropriate values:
- `CLIENT_ID`: Reddit client id
- `CLIENT_SECRET`: Reddit client secret
- `API_KEY:` Twitter API key
- `API_KEY_SECRET`: Twitter API key secret
- `BEARER_TOKEN`: Twitter bearer token
- `INFLUX_URL`: URL to InfluxDB
- `INFLUX_API_TOKEN`: InfluxDB API token
- `ORG`: Organization name
- `SENTIMENT_BUCKET`: Sentiment bucket name
- `TEXT_BUCKET`: Textual data bucket name

### Execution

##### Data Ingestion
1. Launch InfluxDB natively or through docker
```bash
docker run --name influxdb -d \
-p 8086:8086 \
--volume `pwd`/influxdb2:/var/lib/influxdb2 \
--volume `pwd`/config.yml:/etc/influxdb2/config.yml \
influxdb:2.0.7
```
2. Launch RabbitMQ natively or through docker
```bash
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.10-management 
```

3. Start sentiment analysis workers
```bash
# If running on Windows, run with -P solo as other proccess pools don't work
poetry run celery -A data_ingestion.sentiment_analysis.sentiment_analysis worker --loglevel=INFO
```

4. Start aggregators
```bash
poetry run python aggregators/reddit-aggregator.py
poetry run python aggregators/twitter-aggregator.py
```

##### Data Representation
1. Ensure InfluxDB is running
2. Run API
```bash
poetry run uvicorn main:app --reload 
```