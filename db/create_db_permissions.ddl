# First time run:
# sudo mariadb
# Then you can use:
# mariadb -u root -p
CREATE DATABASE inventory;
CREATE USER 'inventory'@'localhost' IDENTIFIED BY 'inventory';
GRANT ALL PRIVILEGES ON *.* TO 'inventory'@'localhost';
FLUSH PRIVILEGES;
