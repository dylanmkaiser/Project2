-- Create and use database
DROP DATABASE IF EXISTS crimes_db;
CREATE DATABASE crimes_db;
USE crimes_db;

-- Create tables for raw data to be loaded into
-- DROP TABLE IF EXISTS;
DROP TABLE IF EXISTS venues;
DROP TABLE IF EXISTS crimes_updated;

CREATE TABLE venues (
  id INT AUTO_INCREMENT,
  venue VARCHAR(50),
  latitude FLOAT,
  longitude FLOAT,
  PRIMARY KEY (id)
);

CREATE TABLE crimes_updated (
  id INT AUTO_INCREMENT,
  dr_number VARCHAR(16),
  date_reported DATE,
  date_occurred DATE,
  time_occurred TIME,
  area_id INT,
  area_name VARCHAR(22),
  crime_description VARCHAR(200),
  address VARCHAR(100),
  latitude FLOAT,
  longitude FLOAT,
  dist_from_staples_center FLOAT,
  dist_from_coliseum FLOAT,
  dist_from_dodger_stadium FLOAT,
  PRIMARY KEY (id)
);