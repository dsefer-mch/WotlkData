
FROM python:3.9

RUN pip3 install --upgrade pip

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

RUN apt-get -y update

RUN apt-get install -y google-chrome-stable

COPY . .

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "src/wotlk_scraper.py"]