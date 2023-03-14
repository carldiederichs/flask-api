#Create a ubuntu base image with python 3 installed.
FROM python:3.8

RUN pip install flask
RUN pip install BeautifulSoup4
RUN pip install requests
RUN pip install word2number
RUN pip install flask_login
RUN pip install --upgrade pip
RUN pip freeze > requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE $PORT

CMD [ "python", "server.py", "rate_limiter.py" ]