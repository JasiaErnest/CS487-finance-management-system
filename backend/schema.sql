-- Finance Management System Database Schema

-- Transactions Table
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY,
    type TEXT,
    amount REAL,
    category TEXT,
    description TEXT,
    date TEXT
);

-- Budgets Table
CREATE TABLE IF NOT EXISTS budgets (
    id INTEGER PRIMARY KEY,
    category TEXT,
    amount REAL,
    period TEXT
);

-- Investments Table
CREATE TABLE IF NOT EXISTS investments (
    id INTEGER PRIMARY KEY,
    name TEXT,
    initial_amount REAL,
    current_value REAL,
    rate REAL,
    date TEXT
);

-- Bills Table
CREATE TABLE IF NOT EXISTS bills (
    id INTEGER PRIMARY KEY,
    name TEXT,
    amount REAL,
    due_date TEXT,
    auto_deduct INTEGER
);
