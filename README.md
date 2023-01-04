This repository details the work done to respond to the assignment presented to SeitaBV within the interview process

The work was realized in a python 3 environment.

The modules used were date time, pandas, flask



The app /gettomorrow route answers the second question
The steps of the resolution are as follows, given predefined thresholds: 
	1. parse today's date and calculte tomorrow's date
	2. filter the values pertinent to tomorrow's date
	3. check in three different functions if the weather is warm, sunny or windy
	4. realize a flask app that asks the user for the date and retuns the api with the required answers
	5. error handling if date is not in table or if information inputted is not a date
