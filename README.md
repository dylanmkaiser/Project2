# Project 2

# Topic: Entertainment & Sports

## Group: Angie, Judy, Dylan

## Our Idea

We think that the Staples Center, Dodger Stadium and the Los Angeles Memorial Coliseum, located in the Los Angeles area, are hotspots for crime. The influx of thousands of people from all over the world to venues that host the Lakers, Clippers, Kings, and countless concerts seem like the type of place that would attract petty theft and other types of crime, as many of the people attending these events are not familiar with the areas surrounding the arena, and where to stay away from. Our goal would be to show that there are more crime incidents in the areas immediately surrounding the three venues, when compared to other areas within a 1.5 mile radius of the venues.

* NOTE: We are analyzing all crimes that occurred between June 1st, 2018 and December 31st, 2018. 

## How would we do this?

We have a data set from the city of LA that lists every crime that occurred in 2018. The link is below.

https://data.lacity.org/A-Safe-City/2018-Crime/cg5b-sjhs

## What are our visualizations?

Our goal would be to have three different visualizations to prove that all three venues either do or do not have an impact on crime rates.

    1. A heat map of all crime incidents in the last 6 months of 2018 within a 1.5 mile radius of each venue.
    2. A plot with 3 lines, one for each venue, that plots the crime count by distance from each venue.
    3. An interactive table that allows users to filter crimes by date, time, etc.

* NOTE: All distances are measured in miles.
* NOTE: All distances are rounded to the nearest tenth.


## mySQL Tables

* venues: contains the venues of interest that are located in Los Angeles and their latitude and longitude
* crimes: contains a division of records number, date reported, date occurred, time, area id, area name, crime description, address, latitude, longitude, distance from Staples Center, distance from Coliseum, and distance from Dodger Stadium

## How to run the app locally:

    1. Sign up for a mapbox token at: https://account.mapbox.com/auth/signup/?route-to=%22/access-tokens/%22
    2. Insert mapbox token into the config.py file: ![1-config file](static/js/config.js)
    3. pip install geopy
    4. Insert sql connection settings in the config.js file: ![2-config file](config.py)
    5. Run the crimes_db.sql file to create the database for the data.
    6. Run the etl.py file.
    7. Run the app.py file.