import tweepy
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    RedirectView,
    FormView,
    TemplateView
)
from django.http import (
    HttpResponse,
    HttpResponseRedirect
)
from django.shortcuts import (
    render,
    redirect
)

from .twitter_auth import (
    auth,
    get_client
)
from .utils import (
    handle_uploaded_file,
    load_tokens_from_file,
    save_tokens_to_file
)
from .forms import PostToTwitterForm


class WelcomePageView(TemplateView):
    template_name = 'post/index.html'


class PostToTwitter(LoginRequiredMixin, FormView):
    form_class = PostToTwitterForm
    success_url = reverse_lazy('post:post_to_twitter')
    template_name = 'post/post_to_twitter.html'

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
                    # file_path = os.path.abspath("./mytwitterbot/media/OIG.jpeg")
                    # Print the file path to check if it's correct
                    # print("File Path:", file_path)

                    # Use API V1 to get media ID
                    auth.set_access_token(access_token, access_secret)
                    client_v1 = tweepy.API(auth)
                    media = client_v1.media_upload(file_path)
                    media_id = media.media_id

                    client.create_tweet(
                        text=content,
                        media_ids=[media_id]
                    )

        except tweepy.errors.TweepyException as e:
            print(f"Twitter API Error: {e}")
            return "Error posting the tweet."
        except Exception as e:
            print(f"Error posting the tweet: {e}")
            return "Error posting the tweet."


class TwitterLogin(RedirectView):
    def get(self, request, *args, **kwargs):
        # Get the Twitter OAuth URL and redirect the user to Twitter for authentication
        try:
            redirect_url = auth.get_authorization_url()
            request.session['request_token'] = auth.request_token
            return redirect(redirect_url)
        except tweepy.errors.TweepyException as e:
            return HttpResponse("Error: %s" % e)


class TwitterCallbackView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return redirect('post:post_to_twitter')

    def get(self, request, *args, **kwargs):
        url = self.get_redirect_url()

        # After the user grants access to your app, this view handles the callback
        verifier = request.GET.get('oauth_verifier')

        # access_token = request.session['request_token']
        access_secret = auth.get_access_token(verifier)

        # Save the user's access_token and access_secret to a file or database
        save_tokens_to_file(access_secret)

        return url
