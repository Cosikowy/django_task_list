FROM python:3.8-slim-buster

ENV DEBUG = True
ENV SECRET_KEY = "@plbmg9$(#+87*nn_pltvr@q_6m0zz9k*bk7@@7q*if4a0w%dq"


RUN mkdir /app
COPY requirements.txt /app

RUN apt-get update 

RUN pip install -r /app/requirements.txt

COPY ./ /app
WORKDIR /app

EXPOSE 8000
RUN python manage.py migrate
