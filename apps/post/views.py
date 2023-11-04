import logging

import tweepy
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin
)
from django.contrib.auth.views import (
    LoginView,
    LogoutView
)
from django.http import (
    HttpResponse,
    HttpResponseRedirect
)
from django.shortcuts import redirect
from django.urls import (
    reverse_lazy,
    reverse
)
from django.views.generic import (
    FormView,
    TemplateView
)
from .forms import (
    PostToTwitterForm,
    LoginForm
)
from .twitter_auth import get_client
from .utils import (
    handle_uploaded_file,
)
from .models import (
    TwitterUsers,
    TweetStatistics
)


class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = 'account/login.html'


class CustomLogoutView(LogoutView):
    template_name = 'account/logout.html'

    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('post:login')


class WelcomePageView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        resistants_count = TwitterUsers.objects.all().count()
        tweets_count = TweetStatistics.objects.all().count()
        context = {'tweets_count': tweets_count, 'resistants_count': resistants_count}
        return self.render_to_response(context)


class TwitterLogin(TemplateView):
    template_name = 'login.html'


class AboutUsView(TemplateView):
    template_name = 'about_us.html'


class PostToTwitter(LoginRequiredMixin, UserPassesTestMixin, FormView):
    form_class = PostToTwitterForm
    success_url = reverse_lazy('post:post_to_twitter')
    template_name = 'post_to_twitter.html'

    def test_func(self):
        return self.request.user.is_superuser

    def get_login_url(self):
        if not self.request.user.is_superuser:
            return super(PostToTwitter, self).get_login_url()
        else:
            return redirect('post:login')

    def post(self, request, *args, **kwargs):
        content = request.POST.get('content', '')
        uploaded_file = request.FILES.get('media_file')
        if content:
            for user in TwitterUsers.objects.all():
                access_token = user.tokens['access_token']
                access_secret = user.tokens['access_secret']
                client = get_client(
                    access_token,
                    access_secret
                )

                try:
                    # Use API V1 to get media ID
                    settings.AUTH.set_access_token(
                        access_token,
                        access_secret
                    )
                    api_v1 = tweepy.API(settings.AUTH)
                    if uploaded_file:
                        # @TODO: the following is for handling Async processing videos uploads
                        # from .tasks import handle_file_upload_process
                        # handle_file_upload_process.delay()
                        media = api_v1.chunked_upload(
                            handle_uploaded_file(
                                uploaded_file
                            ),
                            media_category='tweet_video' if str(uploaded_file).endswith('.mp4') else 'tweet_gif'
                            if str(uploaded_file).endswith('.gif') else 'tweet_image'
                        )
                        media_id = media.media_id
                        statistics = TweetStatistics.objects.create(
                            content=content,
                            uploaded_file_url=uploaded_file,
                            tweet_sent_to=user
                        )
                        statistics.save()
                        client.create_tweet(
                            text=content,
                            media_ids=[media_id]
                        )
                    else:
                        statistics = TweetStatistics(
                            content=content,
                            tweet_sent_to=user
                        )
                        statistics.save()
                        client.create_tweet(
                            text=content,
                        )
                except tweepy.errors.TweepyException as e:
                    logging.error(f"Twitter API Error for {user}: {e}")

                except Exception as e:
                    logging.error(f"Error posting the tweet for {user}: {e}")

        return HttpResponseRedirect(reverse('post:post_to_twitter'))


def twitter_login_sso(request):
    auth = tweepy.OAuth1UserHandler(
        settings.TWITTER_API_KEY,
        settings.TWITTER_API_SECRET_KEY
    )
    try:
        redirect_url = auth.get_authorization_url(signin_with_twitter=True)
        request.session['request_token'] = auth.request_token
        return HttpResponseRedirect(redirect_url)
    except tweepy.errors.TweepyException as e:
        return HttpResponse("Error: %s" % e)


def twitter_callback_sso(request):
    auth = tweepy.OAuth1UserHandler(
        settings.TWITTER_API_KEY,
        settings.TWITTER_API_SECRET_KEY
    )
    verifier = request.GET.get('oauth_verifier')

    request_token = request.session.get('request_token')

    auth.request_token = request_token
    try:
        access_secret = auth.get_access_token(verifier)
        tokens_dict = {
            'access_token': access_secret[0],
            'access_secret': access_secret[1]
        }
        if TwitterUsers.objects.all().exists():
            if access_secret[0] in TwitterUsers.objects.values_list(
                    'tokens__access_token',
                    flat=True
            ).filter():
                return redirect('post:welcome_page')
        users = TwitterUsers.objects.create(tokens=tokens_dict)
        users.save()
    except tweepy.errors.TweepyException as e:
        return HttpResponse("Error: %s" % e)
    return redirect('post:welcome_page')


def health_check(request):
    if request.path == '/healthz':
        return HttpResponse(200)
    return HttpResponse(404)
