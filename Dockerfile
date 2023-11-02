FROM python:3.10@sha256:3c7ae95d95adf492c43da3d998ab8b46894374a7697c2b14f91d252f9a303172

ENV DJANGO_SETTINGS_MODULE=main.settings

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip && pip install -r requirements.txt

RUN mkdir /var/run/gunicorn && mkdir /var/log/gunicorn

RUN touch /var/log/gunicorn/dev.log

EXPOSE  4000

ENTRYPOINT ["gunicorn","-c", "config/gunicorn/config.py"]
#CMD ["gunicorn", "main.wsgi:application", "--bind", "0.0.0.0:4000", "--timeout", "90", "--workers", "3"]

