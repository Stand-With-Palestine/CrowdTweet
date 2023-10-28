from django.db import models


class TwitterUsers(models.Model):
    tokens = models.JSONField(
        default={
            'access_token': '',
            'access_secret': ''
        }
    )

    def __str__(self):
        return f"user {self.id}"
