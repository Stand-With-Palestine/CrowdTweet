from django.conf import settings
import re
import os


def handle_uploaded_file(uploaded_file):
    # Define the directory where you want to save the file, relative to your media root.
    upload_directory = 'uploads/'  # This is a subdirectory within the media root.

    # Protected Man check here !!

    # directory = os.path.basename(uploaded_file)
    # upload_file_name = os.path.splitext(directory)[0]

    # Create the full path for the uploaded file.
    file_path = os.path.join(settings.MEDIA_ROOT, upload_directory, uploaded_file.name)

    # Open the file and save it to the desired location.
    with open(file_path, 'wb') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)

    return file_path

