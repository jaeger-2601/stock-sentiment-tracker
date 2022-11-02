import os
from time import sleep
from celery import Celery
from datetime import datetime, timedelta
from dotenv import load_dotenv
from tweepy import StreamingClient, StreamRule, Tweet
from logging import getLogger
from logging.config import fileConfig

from data_ingestion.stocks import djia_stocks

load_dotenv()

class TwitterRuleError(Exception):
    pass

class TweetAggregator(StreamingClient):

    def __init__(self, *args, **kwargs):

        self.stocks = djia_stocks
        self.rules = self.build_default_rules()
        self.timeout = timedelta(minutes=5)
        self.tweet_count = 0
        self.celery = Celery(
            'data_ingestion.sentiment_analysis.sentiment_analysis', 
            broker='pyamqp://guest@localhost//'
        )
        fileConfig('logging.conf', defaults={'logfilename' : 'logs/twitter.log'})
        self.logger = getLogger('TwitterAggregator')

        self.logger.info('Twitter aggregator initialized')

        super().__init__(*args, **kwargs)

    def build_default_rules(self):

        ticker_rule = ' OR '.join([f'${stock}' for stock in self.stocks.values()])
        name_rule =  ' OR '.join(self.stocks.keys()) 

        return [
            # Cashtag rule to get tweets with stock tickers
            StreamRule(
                f'({ticker_rule}) lang:en'
            ),
            # Name rule to get tweets with company names
            StreamRule(
                f'({name_rule}) lang:en'
            )
        ]
    
    def add_default_rules(self):

        existing_rules = self.get_rules()
        response = None

        # No rules exist
        if existing_rules.data is None:  # type: ignore
            self.logger.info('No rules found. Adding new rules')
            response = self.add_rules(self.rules)
        
        # If rules have changed
        elif set(rule.value for rule in existing_rules.data) != set(rule.value for rule in self.rules):  # type: ignore

            self.logger.info('Rules have changed. Updating existing rules to new rules')
            
            # Delete old rules
            self.delete_rules([ x.id for x in self.get_rules().data])  # type: ignore
            # Add new rules
            response = self.add_rules(self.rules)
        
        # Rules are same
        else:
            self.logger.info('Same stream rules found')
        
        if not response is None and response.data is None :  # type: ignore
            self.logger.critical('Unable to update rules')
            self.logger.critical(f'Twitter rule error: {response.errors[0]["details"]}') # type: ignore
            raise TwitterRuleError(response.errors[0]['details'])  # type: ignore
    
    def on_tweet(self, tweet: Tweet):

        # Send tweet text to analyze and store in DB
        self.celery.send_task(
            'analyze_and_store',
            args=(tweet.text,),
        )
        self.tweet_count += 1
        
        # Log processed tweet counts every 5 minutes
        if datetime.now() > self.end_time:

            self.logger.info(f'Processed {self.tweet_count} tweets in 5 minutes')

            self.end_time = datetime.now() + self.timeout
            self.tweet_count = 0
    
    def on_connection_error(self):

        self.logger.error('Cannot connect to stream')

        return super().on_connection_error()


    def on_errors(self, errors):

        self.logger.error('Errors recieved.')

        for k, v in errors.items():
            self.logger.error(f'{k}: {v}')

        return super().on_errors(errors)
    
    def on_exception(self, exception):

        self.logger.error('An unhandled exception has occured')
        self.logger.exception(exception)

        return super().on_exception(exception)
    
    def run(self):

        backoff = 1

        self.logger.info('Adding default rules')
        self.add_default_rules()

        self.end_time = datetime.now() + self.timeout

        try:

            while True:

                self.logger.info('Starting filter()')
                self.filter()
                self.logger.info(f'Stream disconnected. Backing off for {2 ** backoff} seconds')

                sleep(2 ** backoff)
                backoff += 1

        except KeyboardInterrupt:
            self.logger.critical('Keyboard Interrupt received. Shutting down..')



if __name__ == '__main__':
    tweet_aggregator = TweetAggregator(os.environ['BEARER_TOKEN'], wait_on_rate_limit=True)
    tweet_aggregator.run() 