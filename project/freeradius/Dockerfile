FROM debian:stretch

WORKDIR /project
COPY / /project

RUN apt-get update && apt-get install -y freeradius freeradius-mysql telnet htop

COPY clients.conf /etc/freeradius/3.0/clients.conf
COPY users /etc/freeradius/3.0/users
COPY sql /etc/freeradius/3.0/mods-available
COPY default /etc/freeradius/3.0/sites-enabled

RUN chmod -R o-w /etc/freeradius

WORKDIR /etc/freeradius/3.0/mods-enabled
RUN ["ln", "-s", "../mods-available/sql", "sql"]

COPY cmd.sh /
CMD ["/cmd.sh"]
