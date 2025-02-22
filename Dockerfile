FROM python:3.12-slim

WORKDIR /app

COPY src/ /app/src/
ADD build/requirements.txt .env /app/

RUN  apt-get update \
    && apt-get install gcc -y \
    && apt-get clean \
    && pip install -r /app/requirements.txt \
    && rm -rf /root/.cache/pip
