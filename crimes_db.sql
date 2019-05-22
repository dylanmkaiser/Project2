-- Create and use database
DROP DATABASE IF EXISTS crimes_db;
CREATE DATABASE crimes_db;
USE crimes_db;

-- Create tables for raw data to be loaded into
-- DROP TABLE IF EXISTS;
DROP TABLE IF EXISTS staples_center;
DROP TABLE IF EXISTS coliseum;
DROP TABLE IF EXISTS dodger_stadium;

CREATE TABLE staples_center (
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
  PRIMARY KEY (id)
);

CREATE TABLE coliseum (
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
  dist_from_coliseum FLOAT,
  PRIMARY KEY (id)
);

CREATE TABLE dodger_stadium (
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
  dist_from_dodger_stadium FLOAT,
  PRIMARY KEY (id)
);
