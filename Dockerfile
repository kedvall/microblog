FROM python:3.9
RUN apt-get update && apt-get install -y --no-install-recommends libudev-dev libusb-1.0-0-dev

RUN adduser --gecos "" --disabled-password microblog && echo microblog:blog | chpasswd

WORKDIR /home/microblog

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn pymysql

COPY app app
COPY migrations migrations
COPY microblog.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP=microblog.py

RUN chown -R microblog:microblog ./
USER microblog

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
