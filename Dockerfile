FROM python:3.8

WORKDIR /home
COPY requirements.txt ./

RUN pip install -r requirements.txt && \
    apt-get update && \
    apt-get install -y sqlite3

# Set timezone
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY *.py ./
COPY bot ./bot
COPY share ./share
COPY createdb.sql ./
COPY config.yaml ./
COPY entrypoint.sh ./

ENTRYPOINT ["./entrypoint.sh"]
