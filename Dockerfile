FROM python:3.7

WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY newport_bot_app .
EXPOSE 8000
