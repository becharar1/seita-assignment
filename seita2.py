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
  try:
    time_now = datetime.strptime(now, '%Y-%m-%d')
    time_tomorrow=time_now+timedelta(days=1)
    #specifying thresholds
    warm_threshold=10
    sunny_threshold=100
    windy_threshold=5
    #calculate tomorrow's date
    strtomorrow=str(time_tomorrow.date())
    '''
    here the dataframe for tomorrow's date is extracted
    an error handling mechanism is included that indicates if forecasts are available for this date or no
    '''
    dfdate = df.loc[df['event_start'].str.contains(strtomorrow, case=False)]
    if len(dfdate)>0:
      '''
      if forecasts are available we run three separate programs iwarm, issunny and iswindy
      We return the answer as a string
      '''
      warm=iswarm(dfdate,warm_threshold)
      awarm=""
      if not warm: 
        awarm="not"
      asunny=","
      sunny=issunny(dfdate,sunny_threshold)
      if not sunny:
        asunny="not"
      awindy="and"
      windy=iswindy(dfdate, windy_threshold)
      if not windy:
        awindy="not"
      return "tomorrow's weather is " + awarm + " warm " + asunny +" sunny " +awindy + " windy" 
    else:
      return "No data is available for the chosen date"
  except ValueError:
        return "The entered value is not a date"
    
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
Here we run the flask app with the specified time input
'''
app = Flask(__name__)
@app.route("/gettomorrow/<time>")
def get_now(time):
    return str(get_tomorrow(time))

