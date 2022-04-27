
FROM python:3.9

WORKDIR /App/

RUN pip3 install --upgrade pip

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

RUN apt-get -y update

RUN apt-get install -y google-chrome-stable

# RUN pip3 install selenium
# RUN pip3 install webdriver-manager
# RUN pip3 install urllib3
# RUN pip3 install boto3
# RUN pip3 install pandas
# RUN pip3 install uuid
# RUN pip3 install requests
# RUN pip3 install pillow
# RUN pip3 install datetime
# RUN pip3 install psycopg2-binary
# RUN pip3 install sqlalchemy

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "src/wotlk_scraper.py"]