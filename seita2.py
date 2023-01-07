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
This is the function that gives the forecasts for the day following the specified now
'''
def get_tomorrow(now,df=df):
  
  '''
  The try method studies the presence of a first error namely now that is not in the proper date format
  '''

  dfweather = pd.DataFrame(columns=['warm','sunny','windy'])
  try:
    time_now = datetime.strptime(now, '%Y-%m-%d %H:%M:%S+00')
    time_tomorrow=time_now+timedelta(days=1)
    timestart_tomorrow= datetime(time_tomorrow.year, time_tomorrow.month, time_tomorrow.day,0,0,0)
    min_diff=(timestart_tomorrow-time_now).total_seconds()
    #specifying thresholds
    warm_threshold=10
    sunny_threshold=100
    windy_threshold=5
    #calculate tomorrow's date
    strtomorrow=str(time_tomorrow.date())
    '''
    here the dataframe for tomorrow's date is extracted and filtered with  predictions that are relevant to now's date
    an error handling mechanism is included that indicates if forecasts are available for this date or no
    '''
    dfdate = df.loc[df['event_start'].str.contains(strtomorrow, case=False)]
    dfdate=dfdate.loc[filter_df_beliefs(dfdate, time_now)]
    if len(dfdate)>0:
      '''
      if forecasts are available we run three separate programs iwarm, issunny and iswindy
      We return the answer as a data frame to be later turned into json
      '''
      dfweather.loc['0']=[iswarm(dfdate,warm_threshold),issunny(dfdate,sunny_threshold)
      ,iswindy(dfdate, windy_threshold)]
      return dfweather.to_json(orient = 'records',force_ascii=False,lines=True)   
  except ValueError:
    return None
'''
Here are the three functions iswarm, issunny and iswindy
We consider the temperature warm if one value is higher than the threshold
The same applies for sunny and windy
'''
def iswarm(dfdate:DataFrame,warm_threshold):
  #function get info about temperature
  dftemp=dfdate.loc[dfdate['sensor'] == 'temperature']
  #check if warm: not warm if the threshold is breached once
  i=0
  warm=False
  while i<len(dftemp) and warm==False:
    if dftemp.iloc[i,2] >warm_threshold:
      warm=True
    else:
      i=i+1
  return warm
def issunny(dfdate:DataFrame,sunny_threshold):
  #check if windy: windy if the threshold is breached once
  dfsunny=dfdate.loc[dfdate['sensor'] == 'irradiance']
  #check if sunny: not sunnt if the threshold is breached once
  i=0
  sunny=False
  while i<len(dfsunny) and sunny==False:
    if dfsunny.iloc[i,2] >sunny_threshold:
      sunny=True
    else:
      i=i+1
  return sunny

def iswindy(dfdate:DataFrame,windy_threshold):
    #check if windy: windy if the threshold is breached once
  dfwind=dfdate.loc[dfdate['sensor'] == 'wind speed']
  i=0
  windy=False
  while i<len(dfwind) and windy==False:
    if dfwind.iloc[i,2] >windy_threshold:
      windy=True
    else:
      i=i+1
  return windy
'''
This function filters the beliefs in tomorrow's date to provide only those done at the time now
'''
def filter_df_beliefs(dfdate, time_now):
  dfdiff = pd.DataFrame(columns=['diff'])
  dfdiff.loc[:,'diff']=pd.to_datetime(dfdate.event_start, format='%Y-%m-%d %H:%M:%S+00')
  dfdiff.loc[:,'diff']=(dfdiff['diff']-time_now).dt.total_seconds()
  dfdiff.loc[:,'diff']=dfdate.belief_horizon_in_sec-dfdiff['diff'].astype(int)
  dfdiff.drop(dfdiff[dfdiff['diff']<0].index,inplace=True)
  return (dfdiff.index)
'''
Here we run the flask app with the specified time input
'''
app = Flask(__name__)
@app.route("/gettomorrow/<time>")
def get_now(time):
    return str(get_tomorrow(time))

