FROM python:3.8.3
MAINTAINER Roy LO "RoyLuo@smarter.com.tw"



RUN pip install flask
RUN pip install uwsgi
RUN pip install requests

CMD ["/usr/local/bin/uwsgi", "app.ini"]

