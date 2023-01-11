#Create a ubuntu base image with python 3 installed.
FROM python:3.8

RUN pip install -r requirements.txt

COPY . .

EXPOSE $PORT

CMD [ "python", "server.py" ]