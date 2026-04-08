CREATE DATABASE titan_retail;
USE titan_retail;

-- 1. Products Table
CREATE TABLE products (
    p_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL CHECK (price > 0), -- Schema Check Constraint
    stock INT NOT NULL DEFAULT 0
) ENGINE=InnoDB; -- Ensures ACID support

-- 2. Orders Table (Dependent on Products)
CREATE TABLE orders (
    o_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    quantity INT NOT NULL CHECK (quantity > 0),
    total_price DECIMAL(10,2),
    status ENUM('Pending', 'Completed', 'Cancelled') DEFAULT 'Pending',
    FOREIGN KEY (product_id) REFERENCES products(p_id) ON DELETE CASCADE
) ENGINE=InnoDB;

