FROM python:3.10.11-slim-bullseye

ENV PYTHONUNBUFFERED 1

WORKDIR /code/app

COPY ./requirements.txt /code/requirements.txt
COPY ./Start.sh /usr/bin/Start.sh

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt && \
    mkdir -p /usr/bin/

COPY ./app /code/app
COPY ./yoyo.ini /code/app/

RUN chmod +x /usr/bin/Start.sh

EXPOSE 80

ENTRYPOINT [ "Start.sh" ]
