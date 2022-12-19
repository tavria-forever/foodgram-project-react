FROM python:3.7-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONIOENCODING "UTF-8"

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip3 install -r /app/requirements.txt --no-cache-dir
COPY . .
CMD ["bash", "docker-start.sh"]
