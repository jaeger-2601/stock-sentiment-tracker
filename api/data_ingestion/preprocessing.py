import re
import emoji
import string
import nltk
from nltk.corpus import stopwords

from data_ingestion.stocks import djia_stocks_reverse

try:
    STOPWORDS = stopwords.words("english")
except LookupError:
    nltk.download("stopwords")
    STOPWORDS = stopwords.words("english")


def preprocess_text(text: str) -> str:

    # remove URLs
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"www.\S+", "", text)
    # remove '
    text = text.replace("&#39;", "")
    # remove ampersand
    text = text.replace("&amp;", "")
    # remove quotes
    text = text.replace("&quot;", "")
    # remove ellipsis
    text = text.replace("…", "")
    # remove 's
    text = text.replace("'s", "")
    # remove retweet indicator at start of text
    text = text.lstrip("RT ")
    # demojize
    text = emoji.replace_emoji(text, "")
    return text.strip()


def sentiment_analysis_preprocess(text: str) -> str:

    # remove symbol names
    text = re.sub(r"(\#)(\S+)", r"\2", text)
    text = re.sub(r"(\$)([A-Za-z]+)", r"\2", text)
    # remove usernames
    text = re.sub(r"(u\\)(\S+)", r"\2", text)
    text = re.sub(r"(\@)(\S+)", r"\2", text)

    return text


def text_analysis_preprocess(text: str, company: str) -> str:

    # convert to lower
    text = text.lower()
    # remove cashtag and name
    text = re.sub(f"${company}", "", text)
    text = re.sub(djia_stocks_reverse[company], "", text)
    # remove usernames
    text = re.sub(r"(u\\)(\S+)", "", text)
    text = re.sub(r"(\@)(\S+)", "", text)
    # remove hashtags
    text = re.sub(r"(\#)(\S+)", r"\2", text)
    # remove punctuation
    text = "".join([char for char in text if char not in string.punctuation])
    # remove stop words
    text = " ".join([word for word in text.split() if word not in STOPWORDS])
    # remove numbers
    text = re.sub(r" \d+ ", " ", text)

    return text
