import os
import praw
from time import sleep
from celery import Celery
from typing import Generator
from dotenv import load_dotenv
from datetime import datetime, timedelta

from data_ingestion.stocks import stocks_subreddits

load_dotenv() 

class RedditAggregator:

    def __init__(self, client_id, client_secret):

        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent='Reddit Aggregator'
            )
        self.celery = Celery(
            'data_ingestion.sentiment_analysis.sentiment_analysis', 
            broker='pyamqp://guest@localhost//'
        )

    
    def build_subreddit_instance(self):

        subreddits_rule = '+'.join(stocks_subreddits)
        return self.reddit.subreddit(subreddits_rule)
    
    def aggregate_data(self, timeout:timedelta) -> Generator:

        end_time = datetime.now() + timeout
        subreddit_instance = self.build_subreddit_instance()
        comment_count = 0

        for comment in subreddit_instance.stream.comments():

            comment_count += 1
            self.celery.send_task(
                name='analyze_and_store',
                args=(comment.body,)
            )

            if datetime.now() > end_time:

                yield comment_count
                end_time = datetime.now() + timeout
                comment_count = 0

    
    def run(self):

        for comment_count in self.aggregate_data(timedelta(minutes=5)):

            print(f'Processed {comment_count} reddit comments in 5 minutes')
            #sleep for 1 minute
            sleep(60)

            


if __name__ == '__main__':
    reddit_aggregator = RedditAggregator(os.environ['CLIENT_ID'], os.environ['CLIENT_SECRET'])
    reddit_aggregator.run() 