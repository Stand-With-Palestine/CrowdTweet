from django.contrib import admin
from .models import TwitterUsers, TweetStatistics

admin.site.register(TwitterUsers)
admin.site.register(TweetStatistics)
