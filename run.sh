#!/bin/bash

source config.sh

# Expose ports and run
sudo docker run -it \
        -p $PUBLIC_PORT:8081 \
        -v /home/pi/back-end/hold-configurations:/share/hold-configurations \
        --name $IMAGE_NAME $IMAGE_NAME