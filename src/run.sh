#!/bin/bash

sudo apt-get update
sudo apt-get install docker.io --assume-yes

sudo docker build -t backend .
sudo docker run -d -p 8000:8000 backend 
