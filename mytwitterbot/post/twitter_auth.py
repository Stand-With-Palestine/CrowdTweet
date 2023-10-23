import tweepy


def get_client(ACCESS_TOKEN, ACCESS_TOKEN_SECRET):
    client = tweepy.Client(bearer_token=BEARER_TOKEN,
                           consumer_key=TWITTER_API_KEY,
                           consumer_secret=TWITTER_API_SECRET_KEY,
                           access_token=ACCESS_TOKEN,
                           access_token_secret=ACCESS_TOKEN_SECRET)

    return client
