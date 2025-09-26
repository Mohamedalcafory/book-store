-- Initialize the bookstore database
CREATE DATABASE IF NOT EXISTS bookstore;
USE bookstore;

-- Insert categories
INSERT INTO categories (
    name, description, created_at, updated_at
    ) VALUES (
        'Science Fiction', 
        '', 
        '2025-09-26 21:19:10', 
        '2025-09-26 21:19:10'
    );
INSERT INTO authors (
    name, biography, date_of_birth, country, created_at, updated_at
    ) VALUES (
        'John Doe', 
        'John Doe is a science fiction author', 
        '1990-01-01', 
        'USA', 
        '2025-09-26 21:19:10', 
        '2025-09-26 21:19:10'
    );

-- Create a user for the application
CREATE USER IF NOT EXISTS 'bookstore_user'@'%' IDENTIFIED BY 'bookstore_password';
GRANT ALL PRIVILEGES ON bookstore.* TO 'bookstore_user'@'%';
FLUSH PRIVILEGES;
