import tweepy
from celery.utils.log import get_task_logger
from django.conf import settings

from apps.post.twitter_auth import get_client
from main.celery import app

logger = get_task_logger(__name__)


def get_initialized_client(access_token, access_secret):
    consumer_key = settings.TWITTER_API_KEY
    consumer_secret = settings.TWITTER_API_SECRET_KEY
    client = get_client(
        access_token,
        access_secret
    )
    # Use API V1 to get media ID
    settings.AUTH.set_access_token(
        access_token,
        access_secret
    )
    auth = tweepy.OAuth1UserHandler(consumer_key=consumer_key, consumer_secret=consumer_secret)
    tweepy.API(auth)
    return client


# Usage example

@app.task
def handle_file_upload_process(media_id, content, access_token, access_secret):
    client = get_initialized_client(access_token, access_secret)
    client.create_tweet(
        text=content,
        media_ids=[media_id]
    )
