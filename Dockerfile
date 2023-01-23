FROM ubuntu:latest
COPY . .
RUN apt update && \
    apt install -y cron python3 python3-pip
RUN pip install pytz requests schedule
CMD ["python3", "main.py"]
