import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api."""
    return (
        f"Available Routes:<br>"
        f"/api/v1.0/precipitation<br>"
        f"/api/v1.0/stations<br>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/start<br>"
        f"/api/v1.0/start/end"

    )
@app.route("/api/v1.0/precipitation")
def precipitation():
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= "2016-08-23")

    precipitation = []

    for row in results:
       row_dict = {}
       row_dict["Date"] = row.date
       row_dict["Precipitation"] = row.prcp
       precipitation.append(row_dict)

    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def station():
    stations_results = session.query(Station.station).all()
    stations = list(np.ravel(stations_results))

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    precipitation = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= "2016-08-23").filter(Measurement.date <= "2017-08-23").\
    order_by(Measurement.date.desc()).all()

    tobs_list = list(np.ravel(precipitation))

    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start_only(start=None):
    
    start_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).all()

    print(start_results)

    start_only_list = list(np.ravel(start_results))

    print(start_only_list)

    return jsonify(start_only_list)

@app.route("/api/v1.0/<start>/<end>")
def start_and_end(start=None, end=None):
    
    start_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    print(start_results)

    start_and_end_list = list(np.ravel(start_results))

    print(start_and_end_list)
    
    return jsonify(start_and_end_list)

if __name__ == '__main__':
    app.run(debug=True)