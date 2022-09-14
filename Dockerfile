FROM python:buster

LABEL maintainer="https://github.com/climbar-ai"

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# Add demo app
COPY ./app /app
WORKDIR /app

RUN ls -a

CMD ["python", "./main.py"]