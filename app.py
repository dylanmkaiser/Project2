import os

from datetime import datetime

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from config import mysqlinfo

app = Flask(__name__)

# Database Setup
#################################################

# crimes_db database in mysql
dbname = "crimes_db"

# connection to mysql
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{mysqlinfo['username']}:{mysqlinfo['password']}@{mysqlinfo['host']}:{mysqlinfo['port']}/{dbname}"

db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
venues = Base.classes.venues
crimes = Base.classes.crimes_updated

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")
    
@app.route("/map_index.html")
def map_index():
    """Return the heat map."""
    return render_template("map_index.html")

@app.route("/line_index.html")
def line_index():
    """Return the line plot."""
    return render_template("line_index.html")

@app.route("/venue_coords")
def venue_coords():

    results = db.session.query(venues.latitude, venues.longitude, venues.venue).all()
    coords_list = []
    for result in results:
        coords = {}
        coords["latitude"] = result[0]
        coords["longitude"] = result[1]
        coords["venue"] = result[2]
        coords_list.append(coords)

    return jsonify(coords_list)

@app.route("/crime_coords")
def crime_coords():
    sel = [
        crimes.latitude,
        crimes.longitude
    ]
    results = db.session.query(*sel).all()

    return jsonify(results)

@app.route("/staples_crimes")
def staples_crimes():
    sel = [
        crimes.date_occurred,
        crimes.time_occurred,
        crimes.dist_from_staples_center
    ]

    results = db.session.query(*sel).filter(crimes.dist_from_staples_center <= 1.5).all()

    staples_list = []
    for result in results:
        staples_crime = {}
        staples_crime["date_occurred"] = result[0].strftime("%m/%d/%Y")
        staples_crime["time_occurred"] = result[1].strftime("%H:%M:%S")
        staples_crime["dist_from_venue"] = result[2]
        staples_list.append(staples_crime)

    return jsonify(staples_list)

@app.route("/coliseum_crimes")
def coliseum_crimes():
    sel = [
        crimes.date_occurred,
        crimes.time_occurred,
        crimes.dist_from_coliseum
    ]

    results = db.session.query(*sel).filter(crimes.dist_from_coliseum <= 1.5).all()

    coliseum_list = []
    for result in results:
        coliseum_crime = {}
        coliseum_crime["date_occurred"] = result[0].strftime("%m/%d/%Y")
        coliseum_crime["time_occurred"] = result[1].strftime("%H:%M:%S")
        coliseum_crime["dist_from_venue"] = result[2]
        coliseum_list.append(coliseum_crime)

    return jsonify(coliseum_list)

@app.route("/dodger_crimes")
def dodger_crimes():
    sel = [
        crimes.date_occurred,
        crimes.time_occurred,
        crimes.dist_from_dodger_stadium
    ]

    results = db.session.query(*sel).filter(crimes.dist_from_dodger_stadium <= 1.5).all()

    dodger_list = []
    for result in results:
        dodger_crime = {}
        dodger_crime["date_occurred"] = result[0].strftime("%m/%d/%Y")
        dodger_crime["time_occurred"] = result[1].strftime("%H:%M:%S")
        dodger_crime["dist_from_venue"] = result[2]
        dodger_list.append(dodger_crime)

    return jsonify(dodger_list)

if __name__ == "__main__":
    app.run()