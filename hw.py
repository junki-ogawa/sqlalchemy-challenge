# 1. Import Flask
# Python SQL toolkit and Object Relational Mapper
# import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.pool import StaticPool
import datetime as dt
from flask import Flask, jsonify

# 2. Create an app
app = Flask(__name__)

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# 3. 
#################################################
# Flask Routes
#################################################
@app.route("/")
def index():
    return (
    "CLIMATE APP<br/>"
    "/api/v1.0/precipitation<br/>" 
    "/api/v1.0/stations<br/>"
    "/api/v1.0/tobs<br/>"
    "/api/v1.0/start(yyyy-mm-dd)<br/>"
    "/api/v1.0/start(yyyy-mm-dd)/end(yyyy-mm-dd)<br/>"
    )
# Perform a query to retrieve the date and precipitation scores
@app.route("/api/v1.0/precipitation")
def percip():
    session=Session(engine)
    dandp=session.query(measurement.date,measurement.prcp).all()
    session.close()
    return {d[0]:d[1] for d in dandp}

# Perform a query to retrieve the list of stations
@app.route("/api/v1.0/stations")
def stat():
    session=Session(engine)
    un_stat=session.query(station.station).all()
    session.close()
    return jsonify(station=[s[0]for s in un_stat])

# Perform a query to retrieve dates and temperature observations of the most active station for the last year of data
@app.route("/api/v1.0/tobs")
def tob():
    session=Session(engine)
    oneyrago=dt.date(2017,8,23) - dt.timedelta(days=365*1)
    tobs_data=session.query(measurement.date,measurement.tobs).\
        filter(measurement.date >=oneyrago).\
        filter(measurement.station == "USC00519281").\
        order_by(measurement.date).all()
    session.close()
#create dictionary
    tob_dic= []
    for a in tobs_data:
        row = {a[0]:a[1]}
        tob_dic.append(row)
    return jsonify(tob_dic)

# calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date
@app.route("/api/v1.0/<start>")
def start(start):
#Get min, avg and max for start date that user states
    session=Session(engine)
    results=session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs))\
        .filter(measurement.date>= start).all()
    session.close()
    #Create dictionary for start date
    tobs_start=[]
    for min, max, avg in results:
        tobs_start_dict={}
        tobs_start_dict["min_temp"]=min
        tobs_start_dict["max_temp"]=max
        tobs_start_dict["avg_temp"]=avg
        tobs_start.append(tobs_start_dict)
    return jsonify(tobs_start)

# calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
#Get min, avg and max between start date and end date that user states
    session=Session(engine)
    results= session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs))\
        .filter(measurement.date >= start).filter(measurement.date <= end).all()
    session.close()
    #create dictionary to get the data for max, min, avg in timeframe
    tobs_start_end=[]
    for min, avg, max in results:
        start_end={}
        start_end["min_temp"]=min
        start_end["max_temp"]=max
        start_end["avg_temp"]=avg
        tobs_start_end.append(start_end)
    return jsonify(tobs_start_end)

print (__name__)
# 4. Define main behavior
if __name__ == "__main__":
    app.run(debug=True)