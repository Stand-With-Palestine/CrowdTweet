from django.urls import path
from django.urls.resolvers import URLPattern
from django.views.generic import TemplateView
from . import views

app_name = 'apps.post'

urlpatterns = [
    path('', views.WelcomePageView.as_view(), name='welcome_page'),
    path('post-to-twitter/', views.PostToTwitter.as_view(), name='post_to_twitter'),
    path('login/', views.TwitterLogin.as_view(), name='login'),
    path('twitter-login', views.twitter_login_sso, name='twitter_login'),
    path('callback/', views.twitter_callback_sso, name='twitter_callback'),
]
