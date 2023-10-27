from django.urls import path

from .views import (
    CustomLoginView,
    CustomLogoutView,
    WelcomePageView,
    PostToTwitter,
    TwitterLogin,
    twitter_login_sso,
    twitter_callback_sso,
    AboutUsView
)

app_name = 'apps.post'

urlpatterns = [
    path('', WelcomePageView.as_view(), name='welcome_page'),
    path('post-to-twitter/', PostToTwitter.as_view(), name='post_to_twitter'),
    path('login/', TwitterLogin.as_view(), name='login'),
    path('twitter-login', twitter_login_sso, name='twitter_login'),
    path('callback/', twitter_callback_sso, name='twitter_callback'),
    path('accounts/login/', CustomLoginView.as_view(), name='super_user_login'),
    path('accounts/logout/', CustomLogoutView.as_view(), name='super_user_logout'),
    path('about-us/', AboutUsView.as_view(), name='about_us'),
]
