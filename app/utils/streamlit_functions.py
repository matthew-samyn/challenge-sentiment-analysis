#%%
import regex as re
import pandas as pd
from textblob import TextBlob
from emoji_translate.emoji_translate import Translator
from typing import Tuple
import plotly.express as px
import streamlit as st
import math
import tweepy
import json
import datetime

def scrape_twitter(searchterms, max=700):
    with open("files/twitter_credentials.json", "r") as file:
        credentials = json.loads(file.read())

    auth = tweepy.OAuthHandler(credentials["CONSUMER_KEY"], credentials["CONSUMER_SECRET"])
    auth.set_access_token(credentials["API_KEY"], credentials["API_KEY_SECRET"])
    api = tweepy.API(auth)

    today = datetime.date.today()
    desired_timeformat = "%d-%m-%Y"

    search_dates = [str(today)] + [str(today-datetime.timedelta(num)) for num in range(1,7)]
    print(search_dates)
    tweets_for_df = []

    for search_term in searchterms:
        for date in search_dates:
            public_tweets = api.search_tweets(q=search_term,lang="en",
                                              result_type="mixed", count=100,
                                              until=date)

            for tweet in public_tweets:
                useful_info = [tweet.created_at, tweet.user.screen_name, tweet.text]
                tweets_for_df.append(useful_info)

    df_tweets = pd.DataFrame(data=tweets_for_df,
                             columns=["created_at", "username", "text"])

    print(f"Shape of df before dropping duplicates: {df_tweets.shape}")
    df_tweets = df_tweets.drop_duplicates()
    df_tweets = df_tweets.drop_duplicates(["text"])
    df_tweets = df_tweets[~df_tweets["text"].str.startswith("I've just watched episode S")]
    print(f"Shape of df after dropping duplicates: {df_tweets.shape}")

    if len(df_tweets) > max:
        return df_tweets.iloc[:max]
    else:
        return df_tweets

def preprocess_tweet(tweet):
    """ Function used for a first preprocessing step. """
    hashtag = re.compile(r"^#\S+|\s#\S+")
    at_someone = re.compile(r"^@\S+|\s@\S+")
    url = re.compile(r"https?://\S+")
    tweet_without_hashtag = hashtag.sub(' ', tweet)
    tweet_without_at_and_hashtag = at_someone.sub(' person', tweet_without_hashtag)
    cleaned_text = url.sub(" fan", tweet_without_at_and_hashtag)

    cleaned_text_lower = cleaned_text.strip().lower()
    cleaned_text_lower_splitted = cleaned_text_lower.split()
    if cleaned_text_lower_splitted == "rt":
        cleaned_text_lower = " ".join(cleaned_text_lower_splitted[1:])

    emo = Translator(exact_match_only=False)
    cleaned_text_lower_emojiless = emo.demojify(cleaned_text_lower)

    clean_text = TextBlob(cleaned_text_lower_emojiless).correct()
    return str(clean_text)

def get_tweet_sentiment(tweet):
    # create TextBlob object of tweet text
    analysis = TextBlob(tweet)
    return analysis.polarity

def return_sentiments(df_tweet_column: pd.Series) -> Tuple:
    cleaned_tweets = []
    sentiment_lst = []
    max_progress = df_tweet_column.size
    progress_step = math.ceil(max_progress / 100)
    my_bar = st.progress(0)
    counter = 0
    for tweet in df_tweet_column:
        counter += 1
        # print(counter)
        # print(progress_step)
        percent_complete = math.floor(counter / progress_step)
        # print(percent_complete)
        my_bar.progress(percent_complete)
        cleaned_tweet = preprocess_tweet(tweet)
        cleaned_tweets.append(cleaned_tweet)
        sentiment = get_tweet_sentiment(cleaned_tweet)

        if sentiment > 0:
            sentiment_lst.append("Positive")
        elif sentiment < 0:
            sentiment_lst.append("Negative")
        else:
            sentiment_lst.append("Neutral")
    my_bar.progress(100)
    return sentiment_lst, cleaned_tweets

def show_sentiment_distribution(df_sentiment_column: pd.Series, title):
    sentiment_df = df_sentiment_column.value_counts().to_frame().reset_index()
    sentiment_df.columns = ["sentiment","count"]
    fig = px.pie(sentiment_df, names="sentiment", values="count",
                 hole=.3,title=title)
    return fig
