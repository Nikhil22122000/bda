import tweepy as tw
import numpy as np
import pandas as pd
import os
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from gensim.models import KeyedVectors

def printtweetdata(n, ith_tweet):
        print()
        print(f"Tweet {n}:")
        print(ith_tweet)

    
def getTweets():

    client = tw.Client(bearer_token='XXX')

    # search query for hashtags of sports events
    query_sports_events = '(#ipl) OR (#fifa) OR (#nba) OR (#bbl) OR (#grandslam) lang:en'

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


def KMeans():

    df = pd.read_csv("./sportsEventsTweets.csv")
    tweets = df['text']
    glove_model = KeyedVectors.load_word2vec_format('glove.6B.100d.bin', binary=True)


    # GloVe embedding
    tweet_vectors = []
    for tweet in tweets:
        words = tweet.split()
        vectors = []
        for word in words:
            if word in glove_model:
                vectors.append(glove_model[word])
        if vectors:
            tweet_vectors.append(np.mean(vectors, axis=0))

    # KMeans clustering 
    kmeans = KMeans(n_clusters=5, random_state=0)
    cluster_labels = kmeans.fit_predict(tweet_vectors)
    clusters = [[] for i in range(5)]
    for i, label in enumerate(cluster_labels):
        clusters[label].append(tweets[i])

    return clusters    

if __name__ == "__main__":
    # getTweets()
    clusters = KMeans()
    for i, cluster in enumerate(clusters):
        print('Cluster {}:'.format(i))
        for tweet in cluster:
            print(tweet)
        print('\n')