-- Table for the users applying to the jobs
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL, -- Store hashed passwords, not plain text
    country VARCHAR(100),
    registration_date DATE,
    birth_date DATE,
    nationality VARCHAR(100)
);

-- Table for the companies
CREATE TABLE Companies (
    company_id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(50) UNIQUE NOT NULL,
    industry VARCHAR(50) NOT NULL,
    website VARCHAR(255) NOT NULL,
    description TEXT
);

-- Table for the user's job applications
CREATE TABLE JobApplications (
    application_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    company_id INT,
    FOREIGN KEY (company_id) REFERENCES Companies(company_id)
);

    