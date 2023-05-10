import os
import tweepy as tw
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

consumer_key = os.environ["API_KEY"]
consumer_secret = os.environ["API_KEY_SECRET"]
access_token = os.environ["ACCESS_TOKEN"]
access_token_secret = os.environ["ACCESS_TOKEN_SECRET"]

auth = tw.OAuth1UserHandler(
  consumer_key, 
  consumer_secret, 
  access_token, 
  access_token_secret
)

api = tw.API(auth)


def printtweetdata(n, ith_tweet):
        print()
        print(f"Tweet {n}:")
        print(ith_tweet)

    

client = tw.Client(bearer_token='XXX')

#search query
query1 = 'earthquake lang:en'

start_time = '2023-02-01T00:00:00Z'
end_time = '2023-02-05T23:59:59Z'


db = pd.DataFrame(columns=['id',
                            'text',
                            'created_at'])

i = 1


for tweet in tw.Paginator(client.search_recent_tweets, query=query1,
                                tweet_fields=['created_at'],
                                start_time=start_time,
                                end_time=end_time, 
                                max_results=100).flatten(limit=10):
    
    id = tweet.id
    text = tweet.text
    created_at = tweet.created_at

    ith_tweet = [id, 
                text,
                created_at]

    db.loc[len(db)] = ith_tweet

    printtweetdata(i, ith_tweet)
    i = i+1

output_path='./earthquakeTweets.csv'

db.to_csv(output_path, mode='a', header=not os.path.exists(output_path))


