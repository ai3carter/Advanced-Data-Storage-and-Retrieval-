import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify



# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
# reflect the tables

Base.prepare(engine, reflect=True)
# prepare is mixing the ORM with the engine 
# Save reference to the table
Station = Base.classes.station
Measurement=Base.classes.measurement
# Create our session (link) from Python to the DB



# Flask Setup
app = Flask(__name__)


# Flask Routes


@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    session = Session(engine)
    results = session.query(Measurement.date,Measurement.prcp).all()

    all_prcp = []
    for date,prcp in results:
        prcp_dict={}
        prcp_dict["date"]=date
        prcp_dict["prcp"]=prcp
        all_prcp.append(prcp_dict)
# this list is not a dictionary
    return jsonify(all_prcp)


@app.route("/api/v1.0/stations")
def station():
    
    # Query all stations
    session = Session(engine)
    results = session.query(Station.name).all()
    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))
# this list is not a dictionary
    return jsonify(all_stations)



@app.route("/api/v1.0/tobs")
def tob():
   
    session = Session(engine)
    results = session.query(Measurement.station, Measurement.date,Measurement.tobs).all()

    # Convert list of tuples into normal list
    all_tobs = []
    for station,date,tobs in results:
        tob_dict={}
        tob_dict["station"]=station
        tob_dict["date"]=date
        tob_dict["tobs"]=tobs
        all_tobs.append(tob_dict)

    return jsonify(all_tobs)


@app.route("/api/v1.0/<start>")
def start(start):
    
    start_date=dt.date(start)

    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()

    
    a=func.min(Measurement.tobs)
    b=func.avg(Measurement.tobs)
    c=func.max(Measurement.tobs)

    all_start_tobs = []
    for a,b,c in results:
        start_dict = {}
        start_dict["Max"] = a
        start_dict["Avg"] = b
        start_dict["Min"] = c
        all_start_tobs.append(start_dict)

    return jsonify(all_start_tobs)


@app.route("/api/v1.0/<start>/<end>")
def startend(start,end):

    start_date=dt.date(start)
    end_date=dt.date(end)
    session = Session(engine)
    results=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    
    a=func.min(Measurement.tobs)
    b=func.avg(Measurement.tobs)
    c=func.max(Measurement.tobs)

    all_start_end_tobs = []
    for a,b,c in results:
        start_end_dict = {}
        start_end_dict["Max"] = a
        start_end_dict["Avg"] = b
        start_end_dict["Min"] = c
        all_start_end_tobs.append(start_end_dict)

    return jsonify(all_start_end_tobs)



if __name__ == '__main__':
    app.run(debug=True)
