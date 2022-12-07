#!/bin/sh

echo Starting sentiment analysis workers

# Start sentiment analysis workers
poetry run celery -A data_ingestion.sentiment_analysis.sentiment_analysis worker --loglevel=INFO  --concurrency 3 &

# Start flower for monitoring
poetry run celery -A data_ingestion.sentiment_analysis.sentiment_analysis flower --loglevel=INFO &

# Wait for any process to exit
wait
  
# Exit with status of process that exited first
exit $?