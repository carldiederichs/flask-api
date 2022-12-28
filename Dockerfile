# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /flask-api

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /flask-api

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]