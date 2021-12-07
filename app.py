import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.pool import StaticPool
import datetime as dt
from flask import Flask, jsonify

app = Flask(__name__)

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

measurement = Base.classes.measurement
station = Base.classes.station

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

@app.route("/api/v1.0/tobs")
def tob():
    session=Session(engine)
    minusoneyr =dt.date(2017,8,23) - dt.timedelta(weeks=52)
    tobs_data=session.query(measurement.date,measurement.tobs).\
        filter(measurement.date >=minusoneyr).\
        filter(measurement.station == "USC00519281").\
        order_by(measurement.date).all()
    session.close()

    tob_dic= []
    for a in tobs_data:
        row = {a[0]:a[1]}
        tob_dic.append(row)
    return jsonify(tob_dic)

@app.route("/api/v1.0/precipitation")
def percip():
    session=Session(engine)
    perc=session.query(measurement.date,measurement.prcp).all()
    session.close()
    return {d[0]:d[1] for d in perc}

@app.route("/api/v1.0/stations")
def stat():
    session=Session(engine)
    tion=session.query(station.station).all()
    session.close()
    return jsonify(station=[s[0]for s in tion])

@app.route("/api/v1.0/<start>")
def start(start):
    session=Session(engine)
    results=session.query(func.max(measurement.tobs), func.min(measurement.tobs), func.avg(measurement.tobs))\
        .filter(measurement.date>= start).all()
    session.close()

    ts=[]
    for max, min, avg in results:
        ts_dict={}
        ts_dict["max_temp"]=max
        ts_dict["min_temp"]=min
        ts_dict["avg_temp"]=avg
        ts.append(ts_dict)
    return jsonify(ts)

@app.route("/api/v1.0/<start>/<end>")
def s_e(start, end):
    session=Session(engine)
    results= session.query(func.avg(measurement.tobs), func.min(measurement.tobs), func.max(measurement.tobs))\
        .filter(measurement.date >= start).filter(measurement.date <= end).all()
    session.close()
    t_s_e=[]
    for avg, min, max in results:
        s_e={}
        s_e["max_temp"]=max
        s_e["min_temp"]=min
        s_e["avg_temp"]=avg
        t_s_e.append(s_e)
    return jsonify(t_s_e)


print (__name__)

if __name__ == "__main__":
    app.run(debug=True)