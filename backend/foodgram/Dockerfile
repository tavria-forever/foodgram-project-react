FROM python:3.7-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONIOENCODING "UTF-8"

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY . .
