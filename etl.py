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

#Add empty columns to dataframe
crimes_filtered["dist_from_staples_center"] = ""
crimes_filtered["dist_from_coliseum"] = ""
crimes_filtered["dist_from_dodger_stadium"] = ""

#Staples Center Coordinates
coords_1 = (34.043018, -118.267258)
#Coliseum Coordinates
coords_2 = (34.014053, -118.287872)
#Dodger Stadium Coordinates
coords_3 = (34.073853, -118.239960)

#Function that calculates distance between two coordinates
def distance (coords_1, coords_2):
    value = geopy.distance.distance(coords_1, coords_2).miles
    return value

# Loop through all crimes and calculate distance between each crime and each arena/stadium
for i in range(len(crimes_filtered)):
    coords_1 = (34.043018, -118.267258)
    coords_2 = (34.014053, -118.287872)
    coords_3 = (34.073853, -118.239960)
    lat = crimes_filtered["latitude"][i]
    long = crimes_filtered["longitude"][i]
    crimes_filtered.loc[i, "dist_from_staples_center"] = round(distance(coords_1, (lat, long)), 1)
    crimes_filtered.loc[i, "dist_from_coliseum"] = round(distance(coords_2, (lat, long)), 1)
    crimes_filtered.loc[i, "dist_from_dodger_stadium"] = round(distance(coords_3, (lat, long)), 1)

#Filter out all crimes within a 1.5 mile radius from the Staples Center
staples_center = crimes_filtered.loc[(crimes_filtered["dist_from_staples_center"] <= 1.5), ["dr_number", "date_reported", "date_occurred", "time_occurred",	"area_id", "area_name", "crime_description", "address",	"latitude",	"longitude", "dist_from_staples_center"]].reset_index(drop=True).copy()

#Filter out all crimes within a 1.5 mile radius from the Coliseum
coliseum = crimes_filtered.loc[(crimes_filtered["dist_from_coliseum"] <= 1.5), ["dr_number", "date_reported", "date_occurred", "time_occurred",	"area_id", "area_name", "crime_description", "address",	"latitude",	"longitude", "dist_from_coliseum"]].reset_index(drop=True).copy()

#Filter out all crimes within a 1.5 mile radius from Dodger Stadium
dodger_stadium = crimes_filtered.loc[(crimes_filtered["dist_from_dodger_stadium"] <= 1.5), ["dr_number", "date_reported", "date_occurred", "time_occurred",	"area_id", "area_name", "crime_description", "address",	"latitude",	"longitude", "dist_from_dodger_stadium"]].reset_index(drop=True).copy()


# Connect to mysql database
#-------------------------------------------
db = "crimes_db"

pymysql.install_as_MySQLdb()
rds_connection_string = f"{config.mysqlinfo['username']}:{config.mysqlinfo['password']}@{config.mysqlinfo['host']}:{config.mysqlinfo['port']}/{db}"
engine = create_engine(f'mysql://{rds_connection_string}')

# Upload table 1 info
staples_center.to_sql(name='staples_center', con=engine, if_exists='append', index=False)

# Upload table 2 info
coliseum.to_sql(name='coliseum', con=engine, if_exists='append', index=False)

# Upload table 3 info
dodger_stadium.to_sql(name='dodger_stadium', con=engine, if_exists='append', index=False)
