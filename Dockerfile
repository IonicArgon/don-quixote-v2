# syntax=docker/dockerfile:1

FROM python:3.11.4-bookworm

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ./src .
COPY ./public ./public

CMD ["python3", "main.py"]