FROM ubuntu:latest
COPY . .
RUN apt update && \
    apt install -y cron python3 python3-pip
RUN pip install pytz requests
RUN (crontab -l ; echo "* * * * * python3 main.py") | crontab
RUN service cron start
RUN echo "Start"
CMD ["cron", "-f"]
