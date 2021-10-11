import pandas as pd
import re
from sklearn.model_selection import train_test_split

columns= ["target", "id", "date","flag","user","text"]
df = pd.read_csv("../files/training.1600000.processed.noemoticon.csv",
                 names=columns, encoding='ISO-8859-1')

# Dropping unneeded columns
df = df.drop(["id","date","flag","user"], axis=1)

# Dropping rows that contain a url.
print(df.shape)
df = df[~df["text"].str.contains(r"https?://\S+")]
print(df.shape)

def preprocess_tweet(tweet):
    """ Function used for a first preprocessing step. """
    hashtag = re.compile(r"^#\S+|\s#\S+")
    at_someone = re.compile(r"^@\S+|\s@\S+")
    url = re.compile(r"https?://\S+")
    tweet_without_hashtag = hashtag.sub(' hashtag', tweet)
    tweet_without_at_and_hashtag = at_someone.sub(' person', tweet_without_hashtag)
    cleaned_text = url.sub("", tweet_without_at_and_hashtag)
    cleaned_text_lower = cleaned_text.strip().lower()
    return cleaned_text_lower

train_size = 0.75
val_size = 0.05
random_state=42

df_train_val, df_test = train_test_split(df, test_size=1-train_size-val_size,
                                         random_state=random_state)
df_train, df_val = train_test_split(df_train_val, test_size=val_size / (val_size + train_size),
                                    random_state=random_state)

df_train.reset_index(drop=True).to_csv("../files/train.tsv",sep='\t', index=None, header=None)
df_val.to_csv("../files/val.tsv",sep='\t', index=None, header=None)
df_test.to_csv("../files/test.tsv",sep='\t', index=None, header=None)


