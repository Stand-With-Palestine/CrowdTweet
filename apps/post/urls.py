from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

app_name = 'apps.post'

urlpatterns = [
    path('', views.WelcomePageView.as_view(), name='welcome_page'),
    path('post-to-twitter/', views.PostToTwitter.as_view(), name='post_to_twitter'),
    path('login/', views.TwitterLogin.as_view(), name='twitter_login'),
    path('callback/', views.TwitterCallbackView.as_view(), name='twitter_callback'),
]
