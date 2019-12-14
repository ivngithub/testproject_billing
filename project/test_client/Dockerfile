FROM debian:stretch

WORKDIR /project
COPY / /project

RUN apt-get update && apt-get install -y freeradius telnet htop python3 python3-pip

RUN pip3 install pyrad

COPY dictionary /
COPY dictionary.freeradius /

COPY radclient.py /

COPY start_packet.rad /
COPY stop_packet.rad /
COPY update_packet.rad /
