from celery.utils.log import get_task_logger

from main.celery import app

logger = get_task_logger(__name__)

@app.task
def handle_file_upload_process():
    # @TODO: the follwing is a test task on trigger handle_file_upload_process.delay() >
    #  this will includes the upload file logic
    return 123

