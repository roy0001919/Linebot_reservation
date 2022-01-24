FROM python:3.8.3
MAINTAINER Roy LO "RoyLuo@smarter.com.tw"

WORKDIR /app

ADD . /app

RUN pip install flask
RUN pip install uwsgi
RUN pip install requests
RUN pip install flask_apscheduler
RUN pip install dialogflow

CMD ["/usr/local/bin/uwsgi", "app.ini"]

