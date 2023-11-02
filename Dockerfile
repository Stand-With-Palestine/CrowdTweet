FROM python:3.8

ENV DJANGO_SETTINGS_MODULE=main.settings
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt \
    pip install gunicorn

RUN mkdir /var/run/gunicorn && mkdir /var/log/gunicorn
RUN touch /var/log/gunicorn/dev.log

ENTRYPOINT ["gunicorn","-c", "config/gunicorn/dev.py"]

EXPOSE  8000

# CMD ["gunicorn", "main.wsgi:application", "--bind", "0.0.0.0:8000"]

