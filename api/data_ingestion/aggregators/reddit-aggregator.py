import os
import praw
from celery import Celery
from dotenv import load_dotenv
from datetime import datetime, timedelta
from logging import getLogger
from logging.config import fileConfig

from data_ingestion.stocks import stocks_subreddits

load_dotenv() 

class RedditAggregator:

    def __init__(self, client_id:str, client_secret:str):

        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent='Reddit Aggregator',
            ratelimit_seconds=300
        )
        self.celery = Celery(
            'data_ingestion.sentiment_analysis.sentiment_analysis', 
            broker='pyamqp://guest@localhost//'
        )

        fileConfig('logging.conf', defaults={'logfilename' : 'logs/reddit.log'})
        self.logger = getLogger('RedditAggregator')

        self.logger.info('Reddit aggregator initialized')



    def run(self):

        end_time = datetime.now() + timedelta(minutes=5)
        subreddit_instance = self.reddit.subreddit('+'.join(stocks_subreddits))
        comment_count = 0


        try:

            for comment in subreddit_instance.stream.comments():

                comment_count += 1
                self.celery.send_task(
                    name='analyze_and_store',
                    args=(comment.body,)
                )

                if datetime.now() > end_time:

                    self.logger.info(f'Processed {comment_count} comments in 5 minutes')
                    end_time = datetime.now() + timedelta(minutes=5)
                    comment_count = 0

        except KeyboardInterrupt:
            self.logger.critical('Keyboard Interrupt received. Shutting down..')

if __name__ == '__main__':
    reddit_aggregator = RedditAggregator(os.environ['CLIENT_ID'], os.environ['CLIENT_SECRET'])
    reddit_aggregator.run() 