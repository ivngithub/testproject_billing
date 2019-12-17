FROM debian:stretch

WORKDIR /project
COPY / /project

RUN apt-get update && apt-get install -y freeradius telnet htop python3 python3-pip

RUN pip3 install pyrad
