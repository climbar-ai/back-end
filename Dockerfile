#FROM python:3-buster
#LABEL maintainer="https://github.com/climbar-ai"
#
#WORKDIR /usr/src/app #/app
#
#COPY requirements.txt ./
#RUN pip3 install --no-cache-dir -r requirements.txt
#
#RUN apt-get update -y
#
#RUN apt-get install -y gunicorn3
#
#RUN apt-get update -y
#
#COPY ./app ./ 
##/app
##WORKDIR /usr/src/app #/app
#
#RUN pwd && ls
#
## CMD [ "python", "./your-daemon-or-script.py" ]
#CMD ["gunicorn3", "-b", "0.0.0.0:80", "main:app"] # need to find way to reference variable for port 80 instead of hard coding here

FROM python:alpine

EXPOSE 80

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

RUN apt-get install -y gunicorn3

# Add demo app
COPY ./app /app
WORKDIR /app

CMD ["gunicorn", "-b", "0.0.0.0:80", "main:app"]