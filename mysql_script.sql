CREATE USER IF NOT EXISTS 'clinicapp'@'localhost' IDENTIFIED BY 'clinicapp';
ALTER USER 'clinicapp'@'localhost' IDENTIFIED BY 'clinicapp';
CREATE DATABASE IF NOT EXISTS clinicapp;
GRANT ALL PRIVILEGES ON *.* TO 'clinicapp'@'localhost';
FLUSH PRIVILEGES;
