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

#################################################
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

# maybe you have some global variable for an array

# @app.route("/data")
# def afunction():
#     # Serve up data so your js vizzes can use it

# @app.route("/connect-to-api")
# def anotherfunction():
#     # Connect to the API, get any other data into the database, get it ready to get served

@app.route("/staples_info")
def staples_info():
    """Return coordinates."""

    # Use Pandas to perform the sql query
    sel = [
        staples_center.latitude,
        staples_center.longitude
    ]

    results = db.session.query(*sel).all()

    # staples_coords = {}
    # for result in results:
    #     staples_coords["latitude"] = result[0],
    #     staples_coords["longitude"] = result[1]

    return jsonify(results)

@app.route("/coliseum_info")
def coliseum_info():
    """Return coordinates."""

    # Use Pandas to perform the sql query
    sel = [
        coliseum.latitude,
        coliseum.longitude
    ]

    results = db.session.query(*sel).all()

    return jsonify(results)

@app.route("/dodger_info")
def dodger_info():
    """Return coordinates."""

    # Use Pandas to perform the sql query
    sel = [
        dodger_stadium.latitude,
        dodger_stadium.longitude
    ]

    results = db.session.query(*sel).all()
    
    return jsonify(results)

@app.route("/col")
def col():
    sel = [
        coliseum.dr_number,
        coliseum.date_occurred,
        coliseum.dist_from_coliseum
    ]

    results = db.session.query(*sel).all()
    # print(results)

    col_info = {"date_occurred": ""}
    for result in results:
        col_info["date_occurred"] = result[0]

    return jsonify(col_info)



if __name__ == "__main__":
    app.run()