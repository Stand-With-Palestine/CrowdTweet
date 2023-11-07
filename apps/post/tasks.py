from celery.utils.log import get_task_logger
from main.celery import app

from .models import (
    TwitterUsers,
    TweetStatistics
)
from .utils import handle_uploaded_file

logger = get_task_logger(__name__)


@app.task
def handle_file_upload_process(api_v1, client, content, uploaded_file):
    media = api_v1.chunked_upload(
        handle_uploaded_file(
            uploaded_file
        ),
        media_category='tweet_video' if str(uploaded_file).endswith('.mp4') else 'tweet_gif'
        if str(uploaded_file).endswith('.gif') else 'tweet_image'
    )
    media_id = media.media_id
    client.create_tweet(
        text=content,
        media_ids=[media_id]
    )
