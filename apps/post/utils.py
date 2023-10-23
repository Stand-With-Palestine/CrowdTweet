import re
import os


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


def load_tokens_from_file():
    try:
        file_path = 'tokens_file'
        with open(file_path, 'r') as file:
            lines = file.readlines()
            values = {}
            line_number = 0
            for line in lines:
                # Extract values between single quotes
                values[line_number] = re.findall(r"'(.*?)'", line)
                key1, key2 = values[line_number]
                line_number += 1
        return values
    except Exception as e:
        print(f"Error loading tokens: {e}")
        return None, None


def save_tokens_to_file(access_secret):
    try:
        # Open a file in written mode (you can choose your preferred file path)
        with open('tokens_file', 'a') as file:
            # Write the access token and access secret to the file
            # e.g., file.write(f'Access Token: {access_token}\n')
            file.write(f'Access Secret: {access_secret}\n')

        # Optionally, you can return a success message or perform other actions
        return "Tokens saved successfully."
    except Exception as e:
        # Handle any errors that may occur during file writing
        print(f"Error saving tokens: {e}")
        return "Error saving tokens."
