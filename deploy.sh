#!/bin/bash

ssh root@{ubuntu-api-server-IP} 'rm -r ~/{directory_in_cloud}/{our_project_name}'
scp -r ../{our_project_name} root@{ubuntu-api-server-IP}:~/bookstore

ssh root@{ubuntu-api-server-IP} 'docker stop bookstore-api'
ssh root@{ubuntu-api-server-IP} 'docker rm bookstore-api'

ssh root@{ubuntu-api-server-IP} 'docker build -t bookstore-build ~/bookstore/bookstoreAPI'
ssh root@{ubuntu-api-server-IP} 'docker run -idt -e MODULE_NAME="run" -e PORT="3000" -e PRODUCTION="true" -p 3000:3000 --name=bookstore-api bookstore-build'

ssh root@{ubuntu-api-server-IP} 'docker stop api-nginx'
ssh root@{ubuntu-api-server-IP} 'docker rm api-nginx'
ssh root@{ubuntu-api-server-IP} 'docker build -t bookstore-nginx ~/bookstore/bookstoreAPI/nginx-server-proxy'
# But before writing above cmd on row 13, we have to stop and remove api-nginx
ssh root@{ubuntu-api-server-IP} 'docker run -idt --name=api-nginx -p 80:80 bookstore-nginx'





NOTE TO REMEMBER:
project name is bookstoreAPI (our project name is Bookstore)
directory name on cloud is bookstore
Dockerfile name is bookstore-build
and the Dockerfile is inside ~/bookstore/bookstoreAPI
docker image name is bookstore-api

Dockerfile name is bookstore-nginx
and the Dockerfile is inside ~/bookstore/bookstoreAPI/nginx-server-proxy
docker image name is api-nginx


bookstore-api and api-nginx are same (since both are docker name or docker image name)
bookstore-build and bookstore-nginx both are Dockerfile name








