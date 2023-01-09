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
dfthresholds = pd.DataFrame(columns=['temperature','irradiance','wind speed'])
dfthresholds.loc[0]=[10,100,5]

def get_tomorrow(now,df=df, dfthresholds=dfthresholds):
  '''
  This is the function that gives the forecasts for the day following the specified now
  '''  
  dfweather = pd.DataFrame(columns=['warm','sunny','windy'])
  try:
    time_now = datetime.strptime(now, '%Y-%m-%d %H:%M:%S+00')
  except ValueError:
    return {"Error Message":"The specified date is not in the correct format. Please change"},400
  else:
    #calculate tomorrow's date
    time_tomorrow=time_now+timedelta(days=1)
    '''
    here the dataframe for tomorrow's date is extracted and filtered with  predictions that are relevant to now's date
    an error handling mechanism is included that indicates if forecasts are available for this date or no
    '''
    dfdate = df.loc[df['event_start'].str.contains(str(time_tomorrow.date()), case=False)].sort_values(by=['event_value'])
    dfdate=dfdate.loc[filter_df_beliefs(dfdate, time_now)]
    #print (check_conditions(dfdate))
    if len(dfdate)>0:
      '''
      if forecasts are available we obtain the maximum value for each sensor
      We compare this value to the thresholds. If it is superior than the related condition is true
      '''
      dfweather=(dfdate.groupby('sensor')['event_value'].max()-dfthresholds)>0
      return dfweather.to_json(orient = 'records',force_ascii=False)
    else:
      return {"Error Message":"The specified date is not in the range of dates available. Please change"},400

def filter_df_beliefs(dfdate, time_now):
  '''
  This function filters the beliefs in tomorrow's date to provide only those done at the time now or before that
  This translates into a time difference greater than that of belief horizon in seconds
  '''
  dfdiff = pd.DataFrame(columns=['diff'])
  dfdiff.loc[:,'diff']=(pd.to_datetime(dfdate.event_start, format='%Y-%m-%d %H:%M:%S+00')-time_now).dt.total_seconds()-dfdate.belief_horizon_in_sec
  return (dfdiff.query('diff<0').index)
'''
Here we run the flask app with the specified time input
'''
app = Flask(__name__)
@app.route("/gettomorrow/<time>")
def get_now(time):
    return get_tomorrow(time)
