#!/bin/bash

source config.sh

echo "Image name is: ${IMAGE_NAME}"
echo "APP_PORT: ${APP_PORT}"

#sudo docker build -t ${IMAGE_NAME} .
sudo docker build --build-arg PORT=${APP_PORT} -t ${IMAGE_NAME} .