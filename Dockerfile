FROM python:3.8-slim-buster

ENV DEBIAN_FRONTEND noninteractive

ADD . /opt/

WORKDIR /opt/

RUN apt-get update && apt-get install wget gnupg unzip python3-ipython -y && \
pip3 install -r requirements.txt && \
apt-get update -y && \
apt-get install firefox-esr -y && \
wget https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz && \
tar -xvzf geckodriver-v0.30.0-linux64.tar.gz -C /usr/bin/ && \
apt-get purge -y

CMD python main.py && cd api/ && python main.py
