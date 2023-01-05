from flask import Flask

app = Flask(__name__)
import pandas as pd
df=pd.read_csv("weather.csv", delimiter= ',')
from pandas.io.formats.style_render import DataFrame
from datetime import datetime
from datetime import timedelta
def get_forecasts(now,then,df=df):
  time_now=datetime.strptime(now,'%Y-%m-%d%H:%M:%S')
  time_then=datetime.strptime(then,'%Y-%m-%d%H:%M:%S')
  diff=(time_then-time_now).total_seconds()
  dfthen = df.loc[df['event_start'].str.contains(str(time_then), case=False)]
  dfthen=dfthen.sort_values(by="belief_horizon_in_sec")
  i=0
  ipertinent=0
  dfpertinent = pd.DataFrame(columns=['event_value','sensor','unit'])
  while i<len(dfthen) and ipertinent<3:
    if dfthen.iloc[i,1]>diff:
      dfpertinent.loc[ipertinent]=dfthen.iloc[i,2:5]
      ipertinent+=1
    i=i+1
  if len(dfpertinent)>0:
    return (dfpertinent.to_string())
  else:
    return ("no safe predictions could be made")
@app.route("/")
def hello_world():
    return "Hello, World!"
@app.route("/getforecast/<now>/<then>")
def get_forecast(now, then):
    return (get_forecasts(now, then))
