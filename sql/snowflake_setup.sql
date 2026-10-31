-- ============================================================
-- Snowflake & CoCo Setup Script for FoodMatch
-- Predicts neighborhood fresh produce deficit using free Snowflake Marketplace
-- census and consumer-spending datasets.
-- ============================================================

-- 1. Create dedicated database & schema
CREATE DATABASE IF NOT EXISTS FOODMATCH_DB;
USE DATABASE FOODMATCH_DB;
CREATE SCHEMA IF NOT EXISTS PUBLIC;
USE SCHEMA PUBLIC;

-- 2. Create Warehouse if not exists
CREATE WAREHOUSE IF NOT EXISTS COMPUTE_WH 
WITH WAREHOUSE_SIZE = 'XSMALL' 
AUTO_SUSPEND = 60 
AUTO_RESUME = TRUE;

-- 3. Staging table for Neighborhood Demographics (from Census Marketplace dataset)
CREATE OR REPLACE TABLE neighborhood_demographics (
    zip_code VARCHAR(10) PRIMARY KEY,
    neighborhood_name VARCHAR(100),
    borough VARCHAR(50),
    total_population INT,
    median_household_income FLOAT,
    poverty_rate_pct FLOAT,
    food_insecurity_index FLOAT -- 1.0 (Low) to 10.0 (Extreme)
);

-- 4. Staging table for Weekly Spending Patterns (from Consumer Spending Marketplace dataset)
CREATE OR REPLACE TABLE weekly_food_spending_patterns (
    zip_code VARCHAR(10),
    day_of_week VARCHAR(15), -- Monday .. Sunday
    avg_grocery_spend_per_capita FLOAT,
    avg_fresh_produce_spend_per_capita FLOAT,
    corner_store_count INT,
    supermarket_count INT,
    PRIMARY KEY (zip_code, day_of_week)
);

-- 5. Seed Benchmark Data for NYC Food Deserts (South Bronx, East Harlem, Brownsville)
INSERT INTO neighborhood_demographics VALUES
('10451', 'Concourse Village / Melrose', 'Bronx', 51000, 31200, 34.2, 8.8),
('10455', 'Mott Haven / Port Morris', 'Bronx', 43000, 27500, 38.5, 9.4),
('10027', 'Central / West Harlem', 'Manhattan', 64000, 48000, 22.1, 6.2),
('11212', 'Brownsville', 'Brooklyn', 87000, 29000, 36.8, 9.1),
('10001', 'Chelsea', 'Manhattan', 24000, 115000, 8.5, 2.1);

INSERT INTO weekly_food_spending_patterns VALUES
-- South Bronx (10451): Severe drop in fresh produce supply mid-week to weekend
('10451', 'Monday', 14.50, 1.80, 42, 1),
('10451', 'Tuesday', 13.20, 1.95, 42, 1),
('10451', 'Wednesday', 13.80, 1.60, 42, 1),
('10451', 'Thursday', 15.10, 1.70, 42, 1),
('10451', 'Friday', 22.40, 1.20, 42, 1), -- Peak deficit: high spend volume, nearly 0 fresh produce available
('10451', 'Saturday', 18.00, 2.10, 42, 1),
('10451', 'Sunday', 12.50, 1.50, 42, 1),

-- Mott Haven (10455)
('10455', 'Monday', 13.00, 1.50, 38, 0),
('10455', 'Tuesday', 12.50, 1.60, 38, 0),
('10455', 'Wednesday', 13.10, 1.40, 38, 0),
('10455', 'Thursday', 14.20, 1.30, 38, 0),
('10455', 'Friday', 20.80, 0.90, 38, 0),
('10455', 'Saturday', 16.50, 1.80, 38, 0),
('10455', 'Sunday', 11.20, 1.20, 38, 0);
