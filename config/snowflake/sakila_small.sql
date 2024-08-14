-- Use the specified database and schema
USE DATABASE snowflaketest01;
USE SCHEMA public;

-- Create the country table
CREATE OR REPLACE TABLE snowflaketest01.public.country (
    country_id INTEGER PRIMARY KEY,
    country VARCHAR(50),
    last_update TIMESTAMP_NTZ
);

-- Create the city table
CREATE OR REPLACE TABLE snowflaketest01.public.city (
    city_id INTEGER PRIMARY KEY,
    city VARCHAR(50),
    country_id INTEGER,
    last_update TIMESTAMP_NTZ,
    FOREIGN KEY (country_id) REFERENCES snowflaketest01.public.country(country_id)
);

-- Insert data into the country table
INSERT INTO snowflaketest01.public.country (country_id, country, last_update) 
VALUES
    (20, 'Canada', '2006-02-15 04:44:00'::TIMESTAMP_NTZ),
    (50, 'Japan', '2006-02-15 04:44:00'::TIMESTAMP_NTZ),
    (102, 'United Kingdom', '2006-02-15 04:44:00'::TIMESTAMP_NTZ);

-- Insert data into the city table
INSERT INTO snowflaketest01.public.city (city_id, city, country_id, last_update) 
VALUES
    (312, 'London', 102, '2006-02-15 04:45:25'::TIMESTAMP_NTZ),
    (313, 'London', 20, '2006-02-15 04:45:25'::TIMESTAMP_NTZ),
    (376, 'Okayama', 50, '2006-02-15 04:45:25'::TIMESTAMP_NTZ),
    (377, 'Okinawa', 50, '2006-02-15 04:45:25'::TIMESTAMP_NTZ);