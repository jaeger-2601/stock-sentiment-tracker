import os
from time import sleep
from datetime import datetime, timedelta
from dotenv import load_dotenv
from tweepy import StreamingClient, StreamRule, Tweet

from data_ingestion.stocks import djia_stocks
from data_ingestion.preprocessing import preprocess_twitter_text
from data_ingestion.sentiment_analysis import sentiment_analysis

load_dotenv()

class TwitterRuleError(Exception):
    pass

class TweetAggregator(StreamingClient):

    def __init__(self, *args, **kwargs):

        self.stocks = djia_stocks
        self.rules = self.build_default_rules()
        self.timeout = timedelta(minutes=5)
        self.tweet_count = 0

        super().__init__(*args, **kwargs)

    def build_default_rules(self):

        return [
            # Cashtag rule to get tweets with stock tickers
            StreamRule(
            ' OR '.join([f'${stock}' for stock in self.stocks.values()]) + ' lang:en'
            ),
            # Name rule to get tweets with company names
            StreamRule(
                ' OR '.join(self.stocks.keys()) + ' lang:en'
            ),
        ]
    
    def add_default_rules(self):

        existing_rules = self.get_rules()
        response = None

        # No rules exist
        if existing_rules.data is None:  # type: ignore
            print('No rules found. Adding new rules')
            response = self.add_rules(self.rules)
        
        # If rules have changed
        elif [ rule.value for rule in existing_rules.data] != self.rules:  # type: ignore

            print('Rules have changed')
            
            # Delete old rules
            self.delete_rules([ x.id for x in self.get_rules().data])  # type: ignore
            # Add new rules
            response = self.add_rules(self.rules)
        
        if response.data is None :  # type: ignore
            raise TwitterRuleError(response.errors[0]['details'])  # type: ignore
    
    def on_tweet(self, tweet: Tweet):

        self.tweet_count += 1
        sentiment_analysis.analyze_and_store(
            text=preprocess_twitter_text(tweet.text)
        )

        if datetime.now() > self.end_time:
            self.disconnect()
    
    def run(self):

        self.add_default_rules()

        while True:

            self.end_time = datetime.now() + self.timeout
            self.tweet_count = 0

            self.filter()

            print(f'Processed {self.tweet_count} tweets in 5 minutes')
            sleep(60*10)


if __name__ == '__main__':
    tweet_aggregator = TweetAggregator(os.environ['BEARER_TOKEN'])
    tweet_aggregator.run() 