FROM python:3-alpine

ENV DEVELOPER="Andres Bolaños"

ADD /app home

ADD requirements.txt home

WORKDIR /home

RUN apk add --no-cache --virtual .build-deps gcc musl-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps

# RUN pip install -r requirements.txt

EXPOSE 80

CMD ["python", "app.py"]