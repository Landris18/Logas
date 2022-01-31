FROM python:3.8-slim-buster

ENV DEBIAN_FRONTEND noninteractive

ADD . /root/

WORKDIR /root/

RUN apt-get update && apt-get upgrade -y && apt-get install wget gnupg unzip -y && \
pip3 install -r requirements.txt && \
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list>
apt-get update -y && \
apt-get install google-chrome-stable -y && \
wget https://chromedriver.storage.googleapis.com/97.0.4692.71/chromedriver_linux64.zip && \
unzip chromedriver_linux64.zip -d /usr/bin/ && \
python main.py

expose 1806

CMD python api/main.py
