FROM python:3.8

WORKDIR /home
COPY requirements.txt ./

RUN pip install -r requirements.txt && \
    apt-get update && \
    apt-get install -y sqlite3

COPY *.py ./
COPY bot ./bot
COPY createdb.sql ./
COPY config.yaml ./
COPY entrypoint.sh ./

ENTRYPOINT ["./entrypoint.sh"]
