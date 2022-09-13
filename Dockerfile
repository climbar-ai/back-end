FROM python:buster

LABEL maintainer="https://github.com/climbar-ai"

# Install gunicorn & falcon
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

# Add demo app
COPY ./app /app
WORKDIR /app

CMD ["gunicorn", "-b", "0.0.0.0:80", "main:app"]