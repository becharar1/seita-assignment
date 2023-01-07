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

The usage was realized directly from the command line interface. In order to run this command you can do the following:
	1. download the github repos with the applications and the csv file
	2. install flask dependencies and other required python modules (pandas, datetime)
	2. open the terminal, access the folder and type the following commands:
		- "flask --app seita1 run" for seita1.py
		- "flask --app seita2 run" for seita2.py
	3. In order to interrogate the system open a browser and type the following example:
		- for seita1: http://localhost:5000/getforecast/2020-11-0100:00:00/2020-11-0110:00:00
		- for seita2: http://localhost:5000/gettomorrow/2021-11-01%2000:00:00+00
	4. The results are given in a json format

The files could be containerized as docker images in another installment
