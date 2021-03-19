FROM python:3.7

RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list
RUN apt-get install wget
RUN wget https://dl.google.com/linux/linux_signing_key.pub
RUN apt-get install gnupg
RUN apt-key add linux_signing_key.pub
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable
RUN apt-get install -yqq unzip curl
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/
RUN pip3 install selenium
RUN pip3 install elasticsearch
RUN pip3 install bs4 requests

COPY run.sh /run.sh
COPY daumWork.py /daumWork.py
COPY naverWork.py /naverWork.py

RUN ["chmod", "+x" , "/run.sh"]
CMD ["sh", "/run.sh"]