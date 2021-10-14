import pandas as pd
import tweepy
import json

# Getting login-keys from json.
with open("../app/files/twitter_credentials.json", "r") as file:
    credentials = json.loads(file.read())

auth = tweepy.OAuthHandler(credentials["CONSUMER_KEY"], credentials["CONSUMER_SECRET"])
auth.set_access_token(credentials["API_KEY"], credentials["API_KEY_SECRET"])
api = tweepy.API(auth)

# Tags to search for
to_search_for = ["@nbcbrooklyn99", "#Brooklyn99","#BrooklynNineNine", "Brooklyn Nine-Nine"]

# Dates to search on.
previous_dates = ["10-10-2021","09-10-2021","08-10-2021","07-10-2021","06-10-2021","05-10-2021","04-10-2021"]
tweets_for_df = []

# Loops over all the search terms
for search_term in to_search_for:
    # Loops over all the dates
    for date in previous_dates:
        public_tweets = api.search_tweets(q=search_term,lang="en",
                                          result_type="recent", count=100,
                                          until=date)

        for tweet in public_tweets:
            useful_info = [tweet.created_at, tweet.user.screen_name, tweet.text]
            tweets_for_df.append(useful_info)

df_tweets = pd.DataFrame(data=tweets_for_df,
                         columns=["created_at", "username", "text"])

# Reran this script daily to get more tweets.
df_original = pd.read_csv("../app/files/brooklyn99.csv")

# Appending new tweets with the old ones.
print(f"Shape of df before append: {df_tweets.shape}")
df_tweets = df_tweets.append(df_original)
print(f"Shape of df after append: {df_tweets.shape}")

# Preliminary cleaning
print(f"Shape of df before dropping duplicates: {df_tweets.shape}")
df_tweets = df_tweets.drop_duplicates()
df_tweets = df_tweets.drop_duplicates(["text"],keep=False)
df_tweets = df_tweets[~df_tweets["text"].str.startswith("I've just watched episode S")]
print(f"Shape of df after dropping duplicates: {df_tweets.shape}")

# Saving as .csv
df_tweets.iloc[:200].to_csv("app/files/brooklyn99.csv", index=False)