-- Create the country table
CREATE TABLE country (
    country_id int PRIMARY KEY,
    country varchar(50),
    last_update datetime
);

-- Create the city table
CREATE TABLE city (
    city_id int PRIMARY KEY,
    city varchar(50),
    country_id int FOREIGN KEY REFERENCES country(country_id),
    last_update datetime
);

-- Insert data into the country table
INSERT INTO country (country_id, country, last_update) VALUES
(20, 'Canada', '2006-02-15 04:44:00'),
(50, 'Japan', '2006-02-15 04:44:00'),
(102, 'United Kingdom', '2006-02-15 04:44:00');

-- Insert data into the city table
INSERT INTO city (city_id, city, country_id, last_update) VALUES
(312, 'London', 102, '2006-02-15 04:45:25'),
(313, 'London', 20, '2006-02-15 04:45:25'),
(376, 'Okayama', 50, '2006-02-15 04:45:25'),
(377, 'Okinawa', 50, '2006-02-15 04:45:25');
