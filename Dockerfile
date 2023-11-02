FROM python:3.8

ENV DJANGO_SETTINGS_MODULE=main.settings

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN pip install --upgrade pip poetry==1.6.1 \
    poetry install

RUN pip install gunicorn

COPY . /app

COPY poetry.lock /app/poetry.lock

COPY pyproject.toml /app/pyproject.toml

RUN mkdir /var/run/gunicorn && mkdir /var/log/gunicorn

RUN touch /var/log/gunicorn/dev.log

#ENTRYPOINT ["gunicorn","-c", "config/gunicorn/dev.py"]

EXPOSE  8000

CMD ["gunicorn", "main.wsgi:application", "--bind", "0.0.0.0:8000"]

