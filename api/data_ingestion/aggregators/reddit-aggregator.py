import os
import praw
from time import sleep
from typing import Generator
from dotenv import load_dotenv
from datetime import datetime, timedelta

from data_ingestion.stocks import stocks_subreddits
from data_ingestion.sentiment_analysis.sentiment_analysis import analyze_and_store

load_dotenv() 

class RedditAggregator:

    def __init__(self, client_id, client_secret):

        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent='Reddit Aggregator'
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
            analyze_and_store.delay(
                text=comment.body
            )

            if datetime.now() > end_time:

                yield comment_count
                end_time = datetime.now() + timeout
                comment_count = 0

    
    def run(self):

        for comment_count in self.aggregate_data(timedelta(minutes=5)):

            print(f'Processed {comment_count} reddit comments in 5 minutes')
            #sleep for 10 minutes
            sleep(60*10)

            


if __name__ == '__main__':
    reddit_aggregator = RedditAggregator(os.environ['CLIENT_ID'], os.environ['CLIENT_SECRET'])
    reddit_aggregator.run() 