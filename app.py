import os

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
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{mysqlinfo['username']}:{mysqlinfo['password']}@{mysqlinfo['host']}:{mysqlinfo['port']}/{dbname}"

db = SQLAlchemy(app)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(db.engine, reflect=True)

# Save references to each table
staples_center = Base.classes.staples_center
coliseum = Base.classes.coliseum
dodger_stadium = Base.classes.dodger_stadium

@app.route("/")
def index():
    """Return the homepage."""
    return render_template("index.html")
    
@app.route("/map_index.html")
def map_index():
    """Return the heat map."""
    return render_template("map_index.html")

# @app.route("/connect-to-api")
# def anotherfunction():
#     # Connect to the API, get any other data into the database, get it ready to get served

@app.route("/staples_coords")
def staples_coords():
    """Return coordinates."""

    # Use Pandas to perform the sql query
    sel = [
        staples_center.latitude,
        staples_center.longitude
    ]

    results = db.session.query(*sel).all()

    return jsonify(results)

@app.route("/coliseum_coords")
def coliseum_coords():
    """Return coordinates."""

    # Use Pandas to perform the sql query
    sel = [
        coliseum.latitude,
        coliseum.longitude
    ]

    results = db.session.query(*sel).all()

    return jsonify(results)

@app.route("/dodger_coords")
def dodger_coords():
    """Return coordinates."""

    # Use Pandas to perform the sql query
    sel = [
        dodger_stadium.latitude,
        dodger_stadium.longitude
    ]

    results = db.session.query(*sel).all()
    
    return jsonify(results)

@app.route("/staples_info")
def staples_info():

    results = db.session.query(staples_center.date_occurred, staples_center.time_occurred, staples_center.dist_from_staples_center).all()

    staples_list = []
    for result in results:
        staples_info = {}
        staples_info["date_occurred"] = result[0]
        # staples_info["time_occurred"] = result[1]
        staples_info["dist_from_staples_center"] = result[2]
        staples_list.append(staples_info)

    #print(col_info)
    return jsonify(staples_list)

@app.route("/coliseum_info")
def coliseum_info():

    results = db.session.query(coliseum.date_occurred, coliseum.time_occurred, coliseum.dist_from_coliseum).all()

    col_list = []
    for result in results:
        col_info = {}
        col_info["date_occurred"] = result[0]
        # col_info["time_occurred"] = result[1]
        col_info["dist_from_coliseum"] = result[2]
        col_list.append(col_info)

    return jsonify(col_list)

@app.route("/dodgers_info")
def dodgers_info():

    results = db.session.query(dodger_stadium.date_occurred, dodger_stadium.time_occurred, dodger_stadium.dist_from_dodger_stadium).all()

    dodger_list = []
    for result in results:
        dodger_info = {}
        dodger_info["date_occurred"] = result[0]
        # dodger_info["time_occurred"] = result[1]
        dodger_info["dist_from_dodger_stadium"] = result[2]
        dodger_list.append(dodger_info)

    return jsonify(dodger_list)

if __name__ == "__main__":
    app.run()