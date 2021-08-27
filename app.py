from flask import Flask, jsonify
import sqlalchemy 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import numpy as np
import pandas as pd
import datetime as dt

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect = True)
Station = Base.classes.station
Measurement = Base.classes.measurement
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def index():
    return("Welcome to my app")

@app.route("/api/v1.0/precipitation")
def precipitation():
    last_year = dt.date(2017,8,23)-dt.timedelta(days = 365)

    precip = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_year).all()
    session.close()
    res = {date: prcp for date, prcp in precip}
    return jsonify(res)

@app.route("/api/v1.0/stations")
def stations():
    station_list = session.query(Station.station).all()
    session.close()
    return jsonify([st[0] for st in station_list])

@app.route("/api/v1.0/tobs")
def tobs():
    temperature = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.station == "USC00519281").all()
    session.close()
    return jsonify(temperature)


if __name__ == "__main__":
    app.run(debug = True)
