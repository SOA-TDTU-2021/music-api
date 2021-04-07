FROM python:3.8-alpine
# VOLUME [ "/app" ]
WORKDIR /app
COPY requirements.txt ./
ADD . /app
RUN apk add --no-cache --virtual python3-dev libffi-dev gcc musl-dev make libevent-dev build-base
RUN pip install -r requirements.txt
RUN pip install uwsgi
RUN apk del python3-dev libffi-dev gcc musl-dev make libevent-dev build-base
EXPOSE 9000
CMD [ "uwsgi", "app.ini" ]
