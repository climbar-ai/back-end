#!/bin/bash

source config.sh

# Expose ports and run
#sudo docker run -it \
#        -p $PUBLIC_PORT:$APP_PORT \
#        --name $IMAGE_NAME $IMAGE_NAME
sudo docker run -it \
        -p $PUBLIC_PORT:80 \
        --name $IMAGE_NAME $IMAGE_NAME