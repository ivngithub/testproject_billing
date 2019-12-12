FROM debian:stretch

WORKDIR /project
COPY / /project

RUN apt-get update && apt-get install -y mysql-server telnet htop

RUN sed -i -e"s/^bind-address\s*=\s*127.0.0.1/bind-address = 0.0.0.0/" /etc/mysql/mariadb.conf.d/50-server.cnf

COPY cmd.sh /
CMD ["/cmd.sh"]
