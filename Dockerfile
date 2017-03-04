FROM python:3.5-alpine
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
