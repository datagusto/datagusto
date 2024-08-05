-- Create sequence for auto-increment simulation
CREATE SEQUENCE country_seq START WITH 1 INCREMENT BY 1;

-- Create table `country`
CREATE TABLE country (
  country_id NUMBER(5) GENERATED BY DEFAULT AS IDENTITY,
  country VARCHAR2(50) NOT NULL,
  last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (country_id)
);

-- Insert data into `country`
INSERT INTO country (country_id, country, last_update) VALUES (20, 'Canada', TO_TIMESTAMP('2006-02-15 04:44:00', 'YYYY-MM-DD HH24:MI:SS'));
INSERT INTO country (country_id, country, last_update) VALUES (50, 'Japan', TO_TIMESTAMP('2006-02-15 04:44:00', 'YYYY-MM-DD HH24:MI:SS'));
INSERT INTO country (country_id, country, last_update) VALUES (102, 'United Kingdom', TO_TIMESTAMP('2006-02-15 04:44:00', 'YYYY-MM-DD HH24:MI:SS'));


-- Create sequence for auto-increment simulation
CREATE SEQUENCE city_seq START WITH 1 INCREMENT BY 1;

-- Create table `city`
CREATE TABLE city (
  city_id NUMBER(5) GENERATED BY DEFAULT AS IDENTITY,
  city VARCHAR2(50) NOT NULL,
  country_id NUMBER(5) NOT NULL,
  last_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (city_id),
  CONSTRAINT fk_city_country FOREIGN KEY (country_id) REFERENCES country (country_id) ON DELETE CASCADE
);

-- Insert data into `city`
INSERT INTO city (city_id, city, country_id, last_update) VALUES (312, 'London', 102, TO_TIMESTAMP('2006-02-15 04:45:25', 'YYYY-MM-DD HH24:MI:SS'));
INSERT INTO city (city_id, city, country_id, last_update) VALUES (313, 'London', 20, TO_TIMESTAMP('2006-02-15 04:45:25', 'YYYY-MM-DD HH24:MI:SS'));
INSERT INTO city (city_id, city, country_id, last_update) VALUES (376, 'Okayama', 50, TO_TIMESTAMP('2006-02-15 04:45:25', 'YYYY-MM-DD HH24:MI:SS'));
INSERT INTO city (city_id, city, country_id, last_update) VALUES (377, 'Okinawa', 50, TO_TIMESTAMP('2006-02-15 04:45:25', 'YYYY-MM-DD HH24:MI:SS'));
