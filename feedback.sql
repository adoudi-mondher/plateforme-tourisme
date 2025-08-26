CREATE TABLE feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(150),
    opinion TEXT,
    media_path VARCHAR(255),
    media_type VARCHAR(10),
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
