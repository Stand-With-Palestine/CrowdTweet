from django.urls import path

from . import views
from .views import CustomLoginView, CustomLogoutView

app_name = 'apps.post'

urlpatterns = [
    path('', views.WelcomePageView.as_view(), name='welcome_page'),
    path('post-to-twitter/', views.PostToTwitter.as_view(), name='post_to_twitter'),
    path('login/', views.TwitterLogin.as_view(), name='login'),
    path('twitter-login', views.twitter_login_sso, name='twitter_login'),
    path('callback/', views.twitter_callback_sso, name='twitter_callback'),
    path('accounts/login/', CustomLoginView.as_view(), name='super_user_login'),
    path('accounts/logout/', CustomLogoutView.as_view(), name='super_user_logout'),
]
