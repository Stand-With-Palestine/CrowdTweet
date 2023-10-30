from django.db import models


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
