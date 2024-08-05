CREATE TABLE country (
    country_id INTEGER PRIMARY KEY,
    country VARCHAR(50) NOT NULL,
    last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO country (country_id, country, last_update)
VALUES
    (20, 'Canada', '2006-02-15 04:44:00'),
    (50, 'Japan', '2006-02-15 04:44:00'),
    (102, 'United Kingdom', '2006-02-15 04:44:00');

CREATE TABLE city (
    city_id INTEGER PRIMARY KEY,
    city VARCHAR(50) NOT NULL,
    country_id INTEGER NOT NULL,
    last_update TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (country_id) REFERENCES country(country_id)
);

INSERT INTO city (city_id, city, country_id, last_update)
VALUES
    (312, 'London', 102, '2006-02-15 04:45:25'),
    (313, 'London', 20, '2006-02-15 04:45:25'),
    (376, 'Okayama', 50, '2006-02-15 04:45:25'),
    (377, 'Okinawa', 50, '2006-02-15 04:45:25');
