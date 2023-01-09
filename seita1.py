'''
This suggests that all dependencies have been added
Import all required modules
'''
from flask import Flask
import pandas as pd
from pandas.io.formats.style_render import DataFrame
from datetime import datetime
from datetime import timedelta
df=pd.read_csv("weather.csv", delimiter= ',')
sensors=['temperatre','irradiance','wind speed']
'''
This is the function that enables to get the relevant forecasts
'''
def get_forecasts(now,then,df=df,sensors=sensors): 
  ''' 
  The dates are first parsed from string to datetime
  The difference in time between then and now is calculated
  The data relevant to the specified then date is extracted
  The data is then sorted in ascending order according to timely_beliefs and filtered to remove any forecasts newer than now
  The first measurements relevant to each sensor were extracted from the obtained dataframe
  '''
  time_now=datetime.strptime(now,'%Y-%m-%d%H:%M:%S')
  time_then=datetime.strptime(then,'%Y-%m-%d%H:%M:%S')
  diff=(time_then-time_now).total_seconds()
  dfthen = df.loc[df['event_start'].str.contains(str(time_then), case=False)]
  dfthen_sorted_filtered=dfthen.sort_values(by="belief_horizon_in_sec").query('belief_horizon_in_sec>'+str(diff))
  dfpertinent=dfthen_sorted_filtered.groupby("sensor").first()
  return (dfpertinent.to_json(orient = 'records',force_ascii=False,lines=True))
'''
Here the route is specified using flask with two inputs: now and then
'''
app = Flask(__name__)
@app.route("/getforecast/<now>/<then>")
def get_forecast(now, then):
    return (get_forecasts(now, then))
