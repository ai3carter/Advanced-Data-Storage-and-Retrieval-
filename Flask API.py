import numpy as np

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
# Passenger is from the "station" table
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
def names():
    """Return a list of all passenger names"""
    # Query all passengers
    session = Session(engine)
    results = session.query(Passenger.name).all()
# only one value in it
    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))
# this list is not a dictionary
    return jsonify(all_names)


@app.route("/api/v1.0/stations")
def names():
    """Return a list of all passenger names"""
    # Query all passengers
    session = Session(engine)
    results = session.query(Passenger.name).all()
# only one value in it
    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))
# this list is not a dictionary
    return jsonify(all_names)


@app.route("/api/v1.0/tobs")
def names():
    """Return a list of all passenger names"""
    # Query all passengers
    session = Session(engine)
    results = session.query(Passenger.name).all()
# only one value in it
    # Convert list of tuples into normal list
    all_names = list(np.ravel(results))
# this list is not a dictionary
    return jsonify(all_names)


@app.route("/api/v1.0/<start>")
def passengers():
    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    session = Session(engine)
    results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()
    # ORM query!!!!!!!!!!
# more than one value in it. instead: 3!!!!---create a dictionary
    # Create a dictionary from the row data and append to a list of all_passengers
    all_passengers = []
    for name, age, sex in results:
        passenger_dict = {}
        passenger_dict["name"] = name
        passenger_dict["age"] = age
        passenger_dict["sex"] = sex
        all_passengers.append(passenger_dict)

    return jsonify(all_passengers)


@app.route("/api/v1.0/<start>/<end>")
def passengers():
    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    session = Session(engine)
    results = session.query(Passenger.name, Passenger.age, Passenger.sex).all()
    # ORM query!!!!!!!!!!
# more than one value in it. instead: 3!!!!---create a dictionary
    # Create a dictionary from the row data and append to a list of all_passengers
    all_passengers = []
    for name, age, sex in results:
        passenger_dict = {}
        passenger_dict["name"] = name
        passenger_dict["age"] = age
        passenger_dict["sex"] = sex
        all_passengers.append(passenger_dict)

    return jsonify(all_passengers)



if __name__ == '__main__':
    app.run(debug=True)
