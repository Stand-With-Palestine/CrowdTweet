from django.db import models
from django.db.models import DO_NOTHING, SET_NULL


class TwitterUsers(models.Model):
    tokens = models.JSONField(
        default={
            'access_token': '',
            'access_secret': ''
        }
    )

    def save(self, *args, **kwargs):
        if not self.id:
            # Find the maximum ID in the table and increment it by 1
            max_id = TwitterUsers.objects.aggregate(models.Max('id'))['id__max'] or 0
            self.id = max_id + 1
        super(TwitterUsers, self).save(*args, **kwargs)

    def __str__(self):
        return f"user {self.id}"


class TweetStatistics(models.Model):
    content = models.CharField(max_length=255, blank=True, null=True)
    tweet_sent_to = models.ForeignKey(TwitterUsers, blank=True, null=True, on_delete=SET_NULL)
    uploaded_file_url = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Content {self.content}, Uploaded file URL {self.uploaded_file_url}"
