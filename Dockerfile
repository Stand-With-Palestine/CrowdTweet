FROM python:3.10@sha256:3c7ae95d95adf492c43da3d998ab8b46894374a7697c2b14f91d252f9a303172

ENV DEBIAN_FRONTEND=noninteractive 
ENV DJANGO_SETTINGS_MODULE=main.settings

RUN apt update && apt install -y libmariadb-dev && apt-get -y install gettext

# Create and switch to /app directory
WORKDIR /app

# Copying current directory files to /app in container
COPY . /app

# Installing dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Create a new user
RUN useradd -m runner

# Giving runner user permissions over /app
RUN chown runner:runner /app

# Run the container with the low privileged user
# Comment this line when debugging locally
#USER runner

ENTRYPOINT ["gunicorn","-c", "config/gunicorn/config.py"]
#CMD ["gunicorn", "main.wsgi:application", "--bind", "0.0.0.0:4000", "--timeout", "90", "--workers", "3"]

