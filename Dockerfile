FROM python:3

WORKDIR /home/app

COPY . /home/app

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
