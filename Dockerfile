FROM python:3-alpine

ENV DEVELOPER="Andres Bolaños"

ADD /app home

ADD requirements.txt home

WORKDIR /home

RUN pip install -r requirements.txt

EXPOSE 80

CMD ["python", "app.py"]