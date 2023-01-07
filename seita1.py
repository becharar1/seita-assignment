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
'''
This is the function that enables to get the relevant forecasts
'''
def get_forecasts(now,then,df=df): 
  ''' 
  The dates are first parsed from string to datetime
  The difference in time is calculated
  The data relevant to the specified then date is extracted
  The data is then sorted in ascending order according to timely_beliefs
  '''
  time_now=datetime.strptime(now,'%Y-%m-%d%H:%M:%S')
  time_then=datetime.strptime(then,'%Y-%m-%d%H:%M:%S')
  diff=(time_then-time_now).total_seconds()
  dfthen = df.loc[df['event_start'].str.contains(str(time_then), case=False)]
  dfthen=dfthen.sort_values(by="belief_horizon_in_sec")
  '''
  a loop is here realized to obtain at max the first three forecasts with timely_beliefs greater than the difference
  This corresponds to three most relevant values. The program indicates also if no values are found 
  '''
  i=0
  ipertinent=0
  dfpertinent = pd.DataFrame(columns=['event_value','sensor','unit'])
  while i<len(dfthen) and ipertinent<3:
    if dfthen.iloc[i,1]>diff:
      dfpertinent.loc[ipertinent]=dfthen.iloc[i,2:5]
      ipertinent+=1
    i=i+1
  return (dfpertinent.to_json(orient = 'records',force_ascii=False,lines=True))

'''
Here the route is specified using flask with two inputs: now and then
'''
app = Flask(__name__)
@app.route("/getforecast/<now>/<then>")
def get_forecast(now, then):
    return (get_forecasts(now, then))
