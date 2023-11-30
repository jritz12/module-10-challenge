# Import the dependencies.
import numpy as np
import warnings
warnings.filterwarnings('ignore')
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")



# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Measurements = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
app = Flask(__name__)

#################################################
# Flask Setup
#################################################
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/<br/>"
        f"/api/v1.0/start-end/"
    )




#################################################
# Flask Routes
#################################################
#finds the precipitation data for the previous 12 months
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(func.sum(Measurements.prcp)).\
        filter(Measurements.date<='2017-08-23').\
        filter(Measurements.date>'2016-08-23').\
        group_by(Measurements.date).all()
    session.close()
    all_results = list(np.ravel(results))


    return jsonify(all_results)

#finds the list of stations that are producing the measurements
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Measurements.station).\
        group_by(Measurements.station).all()
    session.close()
    all_results = list(np.ravel(results))


    return jsonify(all_results)
#finds the most active stations for the previous year
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    results = session.query(Measurements.date, Measurements.tobs).\
    filter(Measurements.date<='2017-08-23').\
    filter(Measurements.date>='2016-08-23').\
    filter(Measurements.station =="USC00519281").\
    order_by(Measurements.date).all()

    session.close()
    all_results = list(np.ravel(results))

    return jsonify(all_results)
#finds the min, max, and avg temperature for all date from a given start date until the end of the data set
@app.route("/api/v1.0/start/<start>")
def start(start):
    session = Session(engine)

    results = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).\
        filter(Measurements.date>=start).all()
    session.close()
    all_results = list(np.ravel(results))
    return jsonify(all_results)
#finds the min, max, and avg temperatures for all date between a given start and end date
@app.route("/api/v1.0/start-end/<start>/<end>")
def start_end(start, end):
    session = Session(engine)

    results = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).\
        filter(Measurements.date>=start).\
        filter(Measurements.date<=end).all()
    session.close()
    all_results = list(np.ravel(results))
    return jsonify(all_results)



if __name__ == '__main__':
    app.run(debug=True)
