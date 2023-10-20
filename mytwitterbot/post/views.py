import tweepy
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from .twitter_auth import auth, get_client
import re
import os


########### Welcome page ###############
def index(request):
    return render(request, 'post/index.html')

########## Login and Auhorize Twitter then save tokens to a file ###############

def twitter_login(request):
    # Get the Twitter OAuth URL and redirect the user to Twitter for authentication
    try:
        redirect_url = auth.get_authorization_url()
        request.session['request_token'] = auth.request_token
        return redirect(redirect_url)
    except tweepy.errors.TweepyException as e:
        return HttpResponse("Error: %s" % e)

#@login_required
def twitter_callback(request):
    # After the user grants access to your app, this view handles the callback
    verifier = request.GET.get('oauth_verifier')
    # access_token = request.session['request_token']
    access_secret = auth.get_access_token(verifier)

    # Save the user's access_token and access_secret to a file or database
    save_tokens_to_file(access_secret)

    return redirect('post_to_twitter')  # Redirect to the user's profile page or another page

def save_tokens_to_file(access_secret):
    try:
        # Open a file in write mode (you can choose your preferred file path)
        with open('tokens_file', 'a') as file:
            # Write the access token and access secret to the file
            #file.write(f'Access Token: {access_token}\n')
            file.write(f'Access Secret: {access_secret}\n')
        
        # Optionally, you can return a success message or perform other actions
        return "Tokens saved successfully."
    except Exception as e:
        # Handle any errors that may occur during file writing
        print(f"Error saving tokens: {e}")
        return "Error saving tokens."

################# Read tokens from the file to use the to post #############

def load_tokens_from_file():
    try:
        file_path = ('tokens_file')
        with open(file_path, 'r') as file:
            lines = file.readlines()
            values = {}
            line_number = 0
            for line in lines:
                # print(line)
                # Extract values between single quotes
                values[line_number] = re.findall(r"'(.*?)'", line)
                key1, key2 = values[line_number]
                #print(values[line_number])
                # print("Key 1:", key1)
                # print("Key 2:", key2)
                line_number += 1

        # print(values[1])
        return values
    except Exception as e:
        print(f"Error loading tokens: {e}")
        return None, None

############# Handle uploaded files ################

def handle_uploaded_file(uploaded_file):
    # Define the directory where you want to save the file, relative to your media root.
    upload_directory = 'uploads/'  # This is a subdirectory within the media root.

    # Create the full path for the uploaded file.
    file_path = os.path.join(settings.MEDIA_ROOT, upload_directory, uploaded_file.name)

    # Open the file and save it to the desired location.
    with open(file_path, 'wb') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
    
    return file_path

################## Start for loop to post the tweets ######################

@login_required
def post_to_twitter(request):

    if request.method == 'POST':

        content = request.POST.get('content', '')
        uploaded_file = request.FILES.get('media_file')
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

                    # for or while loop
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

                    # client_v2.create_tweet(text="Tweet text", media_ids=[media_id])

                    client.create_tweet(
                        text=content,
                        media_ids=[media_id]
                        )

            return redirect('post_to_twitter')
            

        except tweepy.errors.TweepyException as e:
            print(f"Twitter API Error: {e}")
            return "Error posting the tweet."
        except Exception as e:
            print(f"Error posting the tweet: {e}")
            return "Error posting the tweet."    

    return render(request, 'post/post_to_twitter.html')