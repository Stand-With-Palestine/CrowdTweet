import tweepy
import requests, os

TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_SECRET_KEY = os.getenv('TWITTER_API_SECRET_KEY')
BEARER_TOKEN = os.getenv('BEARER_TOKEN')

auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET_KEY)

def get_client(ACCESS_TOKEN, ACCESS_TOKEN_SECRET):

    client = tweepy.Client(bearer_token=BEARER_TOKEN,
                            consumer_key=TWITTER_API_KEY,
                            consumer_secret=TWITTER_API_SECRET_KEY,
                            access_token=ACCESS_TOKEN,
                            access_token_secret=ACCESS_TOKEN_SECRET)
    
    return client