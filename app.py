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
session = Session(engine)
# The function will return the max, min, and avg of temperature in the range of 
# the start and end date that you type in
def calc_temps(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()

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

    final_date_query = session.query(func.max(func.strftime("%Y-%m-%d", Measurement.date))).all()
    max_date_string = final_date_query[0][0]
    max_date = dt.datetime.strptime(max_date_string, "%Y-%m-%d")
    begin_date = max_date - dt.timedelta(366)
    results = session.query(func.strftime("%Y-%m-%d",Measurement.date),Measurement.prcp).\
        filter(func.strftime("%Y-%m-%d",Measurement.date)>=begin_date).all()
# strftime translates to 
# "create formatted string for given time/date/datetime object according to specified format."
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
    final_date_query = session.query(func.max(func.strftime("%Y-%m-%d", Measurement.date))).all()
    max_date_string = final_date_query[0][0]
    max_date = dt.datetime.strptime(max_date_string, "%Y-%m-%d")
    begin_date = max_date - dt.timedelta(366)

    results = session.query(Measurement.station, Measurement.date,Measurement.tobs).\
        filter(func.strftime("%Y-%m-%d",Measurement.date)>=begin_date).all()

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
    session = Session(engine)
   
    # find the last day 
    final_date_query = session.query(func.max(func.strftime("%Y-%m-%d", Measurement.date))).all()
    max_date= final_date_query[0][0]
   
    temps=calc_temps(start,max_date)
    
  

    all_start_tobs = []
    date_dict = {'start_date': start, 'end_date': max_date}
    all_start_tobs.append(date_dict)
    all_start_tobs.append({'Observation': 'TMIN', 'Temperature': temps[0][0]})
    all_start_tobs.append({'Observation': 'TAVG', 'Temperature': temps[0][1]})
    all_start_tobs.append({'Observation': 'TMAX', 'Temperature': temps[0][2]})

    return jsonify(all_start_tobs)


@app.route("/api/v1.0/<start>/<end>")
def startend(start,end):

    
    # use the calc_temps func to get the temperatures
    temps=calc_temps(start,end)
    

    #create a list
    return_list = []
    date_dict = {'start_date': start, 'end_date': end}
    return_list.append(date_dict)
    return_list.append({'Observation': 'TMIN', 'Temperature': temps[0][0]})
    return_list.append({'Observation': 'TAVG', 'Temperature': temps[0][1]})
    return_list.append({'Observation': 'TMAX', 'Temperature': temps[0][2]})
    return jsonify(return_list)



if __name__ == '__main__':
    app.run(debug=True)
