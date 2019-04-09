

from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
session.Session(engine)

# Create our session (link) from Python to the DB
app = Flask(__name__)

@app.route("/")
def welcome():
	"""List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/names<precipitation<br/>"
        f"/api/v1.0/names<stations<br/>"
        f"/api/v1.0/names<tobs<br/>"
        f"/api/v1.0/<start><br>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Design a query to retrieve the last 12 months of precipitation data and plot the results

    # Calculate the date 1 year ago from the last data point in the database
    Last_12 = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    prcp_data = session.query(Measurement.date,Measurement.prcp).\
          filter(Measurement.date > one_year_ago).\
         order_by(Measurement.date).all()

         prcp_totals = []
    for result in prcp_data:
        row = {}
        row["date"] = prcp_data[0]
        row["prcp"] = prcp_data[1]
        prcp_totals.append(row)

         return jsonify(dict(prcp_totals))

@app.route("/api/v1.0/stations")
def station():
	station_data = session.query(Measurement).group_by(Measurement.station).count()
	active_stations = session.query(Measurement.station, 
                                func.count(Measurement.station)).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).all()
	 # act_sta = []
    # for st_dict in active_stations:
    #     stat_dict = {}
    #     stat_dict["station"] = st_dict.station
    #     act_sta.append(stat_dict)
     return jsonify(dict(active_stations))

@app.route("/api/v1.0/tobs")
def tobs():
	one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
	year_temp = session.query(Measurement.tobs).\
      filter(Measurement.date >= one_year_ago, Measurement.station == 'USC00519281').\
      order_by(Measurement.tobs).all()

       yr_temp = []
    for y_t in year_temp:
        yrtemp = {}
        yrtemp["tobs"] = y_t.tobs
        yr_temp.append(yrtemp)

    return jsonify(yr_temp)

def calc_start_temps(start_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    
    Args:
        start_date (string): A date string in the format %Y-%m-%d
        end_date (string): A date string in the format %Y-%m-%d
        
    Returns:
        TMIN, TAVE, and TMAX
    """
    
    return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()

@app.route("/api/v1.0/<start>")

def start_date(start):
    calc_start_temp = calc_start_temps(start)
    t_temp= list(np.ravel(calc_start_temp))

    t_min = t_temp[0]
    t_max = t_temp[2]
    t_avg = t_temp[1]
    t_dict = {'Minimum temperature': t_min, 'Maximum temperature': t_max, 'Avg temperature': t_avg}

    return jsonify(t_dict)
 def calc_temps(start_date, end_date):
    """TMIN, TAVG, and TMAX for a list of dates.
    Args:
    start_date (string): A date string in the format %Y-%m-%d
    end_date (string): A date string in the format %Y-%m-%d
    Returns:
    TMIN, TAVE, and TMAX
    """
    return session.query(func.min(Measurement.tobs), \
                         func.avg(Measurement.tobs), \
                         func.max(Measurement.tobs)).\
                         filter(Measurement.date >= start_date).\
                         filter(Measurement.date <= end_date).all()


@app.route("/api/v1.0/<start>/<end>")

def start_end_date(start, end):
    
    calc_temp = calc_temps(start, end)
    ta_temp= list(np.ravel(calc_temp))

    tmin = ta_temp[0]
    tmax = ta_temp[2]
    temp_avg = ta_temp[1]
    temp_dict = { 'Minimum temperature': tmin, 'Maximum temperature': tmax, 'Avg temperature': temp_avg}

    return jsonify(temp_dict)
    



if __name__ == "__main__":
    app.run(debug=True)









