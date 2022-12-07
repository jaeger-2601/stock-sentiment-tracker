#!/bin/sh

echo Starting aggregators

# Start aggregators
poetry run python -m data_ingestion.aggregators.reddit-aggregator &
poetry run python -m data_ingestion.aggregators.twitter-aggregator &

# Wait for any process to exit
wait
  
# Exit with status of process that exited first
exit $?