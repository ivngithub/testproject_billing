#!/bin/bash

/usr/bin/mysqld_safe &
sleep 10s
echo "GRANT ALL ON *.* TO root@'%' IDENTIFIED BY 'changeme' WITH GRANT OPTION; FLUSH PRIVILEGES" | mysql
mysql -uroot < project/mysql/create_radius_db.sql && mysql -uroot radius < project/mysql/schema.sql && mysql -uroot radius < project/mysql/setup.sql && mysql -uroot radius < project/mysql/users.sql
echo "GRANT ALL PRIVILEGES ON *.* To 'root'@'%' IDENTIFIED BY 'passwd';" | mysql
killall mysqld
sleep 10s
/usr/bin/mysqld_safe
