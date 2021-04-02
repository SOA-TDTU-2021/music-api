FROM python:3.9.2-alpine3.13
# VOLUME [ "/app" ]
WORKDIR /app
COPY requirements.txt ./
ADD . /app
RUN apk add --no-cache --virtual .build-deps \
        gcc libc-dev linux-headers \
    ; \
    pip install -r requirements.txt; \
    apk del .build-deps
EXPOSE 9000
CMD [ "uwsgi", "app.ini" ]
