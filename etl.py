import pandas as pd
import numpy as np
import pandas as pd
import numpy as np
import geopy.distance
import datetime
datetime.datetime.strptime
from sqlalchemy import create_engine

# PyMySQL 
import pymysql
import config


df = pd.read_csv("crimedata.csv")

#Filter out necessary columns
crimes_df = df[["DR Number", "Date Reported", "Date Occurred", "Time Occurred", "Area ID", "Area Name", "Crime Code Description", "Address", "Latitude", "Longitude"]].copy()

#Filter for crimes that occurred only in surrounding areas of the arenas/stadiums
crimes_filtered = crimes_df.loc[(crimes_df["Area Name"] != "Topanga") & (crimes_df["Area Name"] != "Van Nuys") 
                        & (crimes_df["Area Name"] != "West Valley") & (crimes_df["Area Name"] != "Foothill")
                        & (crimes_df["Area Name"] != "Devonshire") & (crimes_df["Area Name"] != "Harbor") 
                            & (crimes_df["Area Name"] != "West LA") & (crimes_df["Area Name"] != "Pacific") 
                            & (crimes_df["Area Name"] != "Mission") & (crimes_df["Area Name"] != "N Hollywood") 
                            & (crimes_df["Area Name"] != "Hollywood") & (crimes_df["Area Name"] != "Wilshire") 
                            & (crimes_df["Area Name"] != "Southeast")]

#Reset index
crimes_filtered = crimes_filtered.reset_index(drop=True)

#Change the date columns into datetime objects
crimes_filtered['Date Occurred'] =  pd.to_datetime(crimes_filtered['Date Occurred'], format='%m/%d/%y')
crimes_filtered['Date Reported'] =  pd.to_datetime(crimes_filtered['Date Reported'], format='%m/%d/%y')

#Filter for crimes that occurred in the second half of 2018
crimes_filtered = crimes_filtered[(crimes_filtered['Date Occurred'] >= '2018-06-01') & (crimes_filtered['Date Occurred'] <= '2018-12-31')].reset_index(drop=True)

crimes_filtered = crimes_filtered.rename(columns={"DR Number": "dr_number", "Date Reported": "date_reported", "Date Occurred": "date_occurred", "Time Occurred": "time_occurred", "Area ID": "area_id",
    "Area Name": "area_name", "Crime Code Description": "crime_description", "Address": "address", "Latitude": "latitude", "Longitude": "longitude"})


venues = pd.DataFrame([
    {"venue": "staples_center", "latitude": 34.043018, "longitude": -118.267258},
    {"venue": "coliseum", "latitude": 34.014053, "longitude": -118.287872},
    {"venue": "dodger_stadium", "latitude": 34.073853 , "longitude": -118.239960}])
venues = venues[["venue", "latitude", "longitude"]]

#Function that calculates distance between two coordinates
def distance (coords_1, coords_2):
    value = geopy.distance.distance(coords_1, coords_2).miles
    return value

for i in range(len(crimes_filtered)):
    for j in range(len(venues_df)):
        venue_coords = (venues_df["latitude"][j], venues_df["longitude"][j])
        venue_name = "dist_from_" + venues_df["venue"][j]
        crime_coords = (crimes_filtered["latitude"][i], crimes_filtered["longitude"][i])
        crimes_filtered.loc[i, venue_name] = round(distance(venue_coords, crime_coords), 1)

#Filter out all crimes within a 1.5 mile radius from at least one of the venues
crimes_updated = crimes_filtered.loc[(crimes_filtered["dist_from_staples_center"] <= 1.5) | (crimes_filtered["dist_from_coliseum"] <= 1.5) | (crimes_filtered["dist_from_dodger_stadium"] <= 1.5), :].reset_index(drop=True).copy()

# Connect to mysql database
#-------------------------------------------
db = "crimes_db"

pymysql.install_as_MySQLdb()
rds_connection_string = f"{config.mysqlinfo['username']}:{config.mysqlinfo['password']}@{config.mysqlinfo['host']}:{config.mysqlinfo['port']}/{db}"
engine = create_engine(f'mysql://{rds_connection_string}')

# Upload table 1 info
venues.to_sql(name='venues', con=engine, if_exists='append', index=False)

# Upload table 2 info
crimes_updated.to_sql(name='crimes_updated', con=engine, if_exists='append', index=False)

