# reference: https://github.com/berndverst/falcon-docker/blob/master/Dockerfile and https://github.com/climbar-ai/back-end/blob/main/Dockerfile

FROM python:buster

LABEL maintainer="https://github.com/climbar-ai"

# Install gunicorn & falcon
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# Add demo app
COPY ./app /app
#COPY ./config.sh /app/config.sh
WORKDIR /app

RUN ls -a

#CMD gunicorn -b 0.0.0.0:${APP_PORT} main:app # find way to make this shell variable work
CMD ["gunicorn", "-b", "0.0.0.0:80", "main:app"]