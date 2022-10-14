import re
import emoji
import string
import nltk
from nltk.corpus import stopwords

from data_ingestion.stocks import djia_stocks

nltk.download('stopwords')
STOPWORDS = stopwords.words('english')

def preprocess_twitter_text(text:str) -> str:

    # remove URLs
    text = re.sub(r'https?://\S+', "", text)
    text = re.sub(r'www.\S+', "", text)
    # remove '
    text = text.replace('&#39;', "'")
    # remove symbol names
    text = re.sub(r'(\#)(\S+)', r'hashtag_\2', text)
    text = re.sub(r'(\$)([A-Za-z]+)', r'cashtag_\2', text)
    # remove usernames
    text = re.sub(r'(\@)(\S+)', r'mention_\2', text)
    # demojize
    text = emoji.demojize(text, delimiters=("", " "))

    return text.strip()

def preprocess_reddit_text(text:str) -> str:

    # remove URLs
    text = re.sub(r'https?://\S+', "", text)
    text = re.sub(r'www.\S+', "", text)
    # remove '
    text = text.replace('&#39;', "'")
    # demojize
    text = emoji.demojize(text, delimiters=("", " "))
    # remove usernames
    text = re.sub(r'(u\\)(\S+)', r'mention_\2', text)
    # remove punctuation
    text  = "".join([char for char in text if char not in string.punctuation])

    return text.strip()

def remove_uneccesary_words(text, company):

    # remove cashtags
    text = re.sub(r'(cashtag_)(\S+)', '', text)
    # remove mentions
    text = re.sub(r'(mention_)(\S+)', '', text)
    # remove hashtags
    text = re.sub(r'(hashtag_)(\S+)', '', text)
    # remove company names
    text = re.sub(f'( {"|".join(djia_stocks.values())} )', '', text)
    # remove stop words
    text = re.sub(f'( {"|".join(STOPWORDS)} )', '', text)

    return text