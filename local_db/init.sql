-- Table for Users
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL, -- Store hashed passwords, not plain text
    country VARCHAR(50),
    registration_date DATETIME DEFAULT CURRENT_TIMESTAMP
);

