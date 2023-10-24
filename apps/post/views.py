import tweepy
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import (
    HttpResponse, HttpResponseRedirect
)
from django.shortcuts import (
    redirect
)
from django.urls import reverse_lazy
from django.views.generic import (
    View,
    FormView,
    TemplateView
)

from .forms import PostToTwitterForm
from .twitter_auth import (
    get_client
)
from .utils import (
    handle_uploaded_file,
    load_tokens_from_file,
    save_tokens_to_file
)


class WelcomePageView(TemplateView):
    template_name = 'index.html'


class PostToTwitter(LoginRequiredMixin, FormView):
    form_class = PostToTwitterForm
    success_url = reverse_lazy('post:post_to_twitter')
    template_name = 'post_to_twitter.html'

    def post(self, request, *args, **kwargs):
        content = request.POST.get('content', '')
        uploaded_file = request.FILES.get('media_file')
        file_path = ''
        if uploaded_file:
            # Save the uploaded file to the specified directory.
            file_path = handle_uploaded_file(uploaded_file)
            print("File Path:", file_path)
        try:
            if content:
                print('Content:', content)
                values = load_tokens_from_file()
                for value in values:
                    access_token, access_secret = values[value]

                    client = get_client(access_token, access_secret)

                    # Get the absolute path to the media/OIG.jpeg file
                    # file_path = os.path.abspath("./main/media/OIG.jpeg")
                    # Print the file path to check if it's correct
                    # print("File Path:", file_path)

                    # Use API V1 to get media ID
                    settings.AUTH.set_access_token(access_token, access_secret)
                    client_v1 = tweepy.API(settings.AUTH)
                    media = client_v1.media_upload(file_path)
                    media_id = media.media_id

                    client.create_tweet(
                        text=content,
                        media_ids=[media_id]
                    )
                    return redirect('post:welcome_page')

        except tweepy.errors.TweepyException as e:
            print(f"Twitter API Error: {e}")
            return "Error posting the tweet."
        except Exception as e:
            print(f"Error posting the tweet: {e}")
            return "Error posting the tweet."


class TwitterLogin(View):

    def get(self, request):
        try:
            auth = tweepy.OAuth1UserHandler(settings.TWITTER_API_KEY, settings.TWITTER_API_SECRET_KEY)
            redirect_url = auth.get_authorization_url()
            request.session['request_token'] = auth.request_token
            return HttpResponseRedirect(redirect_url)
        except tweepy.errors.TweepyException as e:
            return HttpResponse("Error: %s" % e)


class TwitterCallbackView(View):

    def get(self, request):
        verifier = request.GET.get('oauth_verifier')

        request_token = request.session.get('request_token')

        settings.AUTH.request_token = request_token
        try:
            access_secret = settings.AUTH.get_access_token(verifier)
            # Save the user's access_token and access_secret to a file or database
            save_tokens_to_file(access_secret)
            return redirect('post:welcome_page')
        except tweepy.errors.TweepyException as e:
            return HttpResponse("Error: %s" % e)
