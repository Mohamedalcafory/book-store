-- Initialize the bookstore database
CREATE DATABASE IF NOT EXISTS bookstore;
USE bookstore;

-- Create a user for the application
CREATE USER IF NOT EXISTS 'bookstore_user'@'%' IDENTIFIED BY 'bookstore_password';
GRANT ALL PRIVILEGES ON bookstore.* TO 'bookstore_user'@'%';
FLUSH PRIVILEGES;
