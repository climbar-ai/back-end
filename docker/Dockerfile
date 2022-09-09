FROM python:3
LABEL maintainer="https://github.com/climbar-ai"

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

RUN apt-get update -y

# RUN apt-get install -y gunicorn3

# RUN apt-get update -y

COPY ./app /app
WORKDIR /app

# CMD [ "python", "./your-daemon-or-script.py" ]
CMD ["gunicorn3", "-b", "0.0.0.0:80", "main:app"] # need to find way to reference variable for port 80 instead of hard coding here