import pandas as pd
from twython import Twython

CONSUMER_KEY = '####'
CONSUMER_SECRET = '####'
OAUTH_TOKEN = '####'
OAUTH_TOKEN_SECRET = '####'
twitter = Twython(
    CONSUMER_KEY, CONSUMER_SECRET,
    OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

tweets_ids = pd.read_csv('ids.csv')

tweets = []

tweets_ids = tweets_ids[:20]

for id_of_tweet in tweets_ids['id']:
    try:
        print(tweet)
        tweet = twitter.show_status(id=id_of_tweet)
        tweets.append(tweet)
    except:
        continue

col_names = ['created_at', 'id', 'id_str', 'text', 'truncated', 'entities',
             'source', 'in_reply_to_status_id', 'in_reply_to_status_id_str',
             'in_reply_to_user_id', 'in_reply_to_user_id_str', 'in_reply_to_screen_name',
             'user', 'geo', 'coordinates', 'place', 'contributors', 'retweeted_status',
             'is_quote_status', 'retweet_count', 'favorite_count', 'favorited', 'retweeted', 'lang']

df = pd.DataFrame(tweets, columns=col_names)

df.to_csv('tweets.csv', index=False)