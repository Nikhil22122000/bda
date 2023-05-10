import os
import tweepy as tw
import pandas as pd


def printtweetdata(n, ith_tweet):
        print()
        print(f"Tweet {n}:")
        print(ith_tweet)

    
def getTweets():

    client = tw.Client(bearer_token='XXX')

    # search query for hashtags of sports events
    query_sports_events = '(#ipl) OR (#fifa) OR (#nba) lang:en'

    start_time = '2023-03-25T00:00:00Z'
    end_time = '2023-03-30T23:59:59Z'


    db = pd.DataFrame(columns=['id',
                                'text',
                                'created_at'])

    i = 1


    for tweet in tw.Paginator(client.search_recent_tweets, query=query_sports_events,
                                    tweet_fields=['created_at'],
                                    start_time=start_time,
                                    end_time=end_time, 
                                    max_results=100).flatten(limit=500):
        
        id = tweet.id
        text = tweet.text
        created_at = tweet.created_at

        ith_tweet = [id, 
                    text,
                    created_at]

        db.loc[len(db)] = ith_tweet

        printtweetdata(i, ith_tweet)
        i = i+1

    output_path='./sportsEventsTweets.csv'

    db.to_csv(output_path, mode='a', header=not os.path.exists(output_path))


def decayingWindowAlgo():
    df = pd.read_csv("./sportsEventsTweets.csv")
    tweets = df['text']
    # calculating weights
    const = 0.1

    ipl = 0
    for tweet in tweets:
        if "ipl" in tweet:
            ipl = ipl*(1-const) + 1
        else:
            ipl = ipl*(1-const) + 0

    fifa = 0
    for tweet in tweets:
        if "fifa" in tweet:
            fifa = fifa*(1-const) + 1
        else:
            fifa = fifa*(1-const) + 0

    nba = 0
    for tweet in tweets:
        if "nba" in tweet:
            nba = nba*(1-const) + 1
        else:
            nba = nba*(1-const) + 0


    # finding the popular tweets
    popular_sport = "#"
    if(ipl > fifa and ipl > nba):
        popular_sport += "ipl"
    elif(fifa > ipl and fifa > nba):
        popular_sport += "fifa"
    else:
        popular_sport += "nba"


    popular_tweets = []
    for tweet in tweets:
        if popular_sport in tweet:
            popular_tweets.append(tweet)
    
    return popular_sport, popular_tweets


if __name__ == "__main__":
    # getTweets()
    popular_sport, popular_tweets = decayingWindowAlgo()
    print("Popular sport is: ", popular_sport)
    print("Popular Tweets are: ")
    for tweet in popular_tweets:
        print(tweet)
