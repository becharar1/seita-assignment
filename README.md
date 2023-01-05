This repository details the work done to respond to the assignment presented to SeitaBV within the interview process

The work was realized in a python 3 environment.

The modules used were date time, pandas, flask

seita1.py route answers the first question:
The steps of the resolution are as follows:
	1. given a date now and date then
	2. Calculate the difference between the two dates
	3. Obtain the data relevant for the then date
	4. Sort the data by increasing timely_beliefs
	5. Check for timely_beliefs that are in the range of the calculated difference
	6. Provide at max the three first forecasts, if not indicate that there are no forecasts available
	6. Little to no error handling was realized for this project

seita2.py route answers the second question
The steps of the resolution are as follows:
	1. given a date and predefined thresholds: 
	2. parse today's date and calculte tomorrow's date
	3. filter the values pertinent to tomorrow's date
	4. check in three different functions if the weather is warm, sunny or windy
	5. realize a flask app that asks the user for the date and retuns the api with the required answers
	6. error handling if date is not in table or if information inputted is not a date
