import requests
import json
import time

# Gets data from OpenWeather API, returns in dictionary
def queryWeather(url):
	API_reply = requests.get(url)
	reply_json = API_reply.json()

	state = dict(
		city = reply_json['name'],
		cond = reply_json['weather'][0]['description'],
		cond_ID = reply_json['weather'][0]['id'],
		temp = reply_json['main']['temp'],
		windspeed = reply_json['wind']['speed']
	)

	return state

# Determines wheel location. IDs are from OpenWeather
def mapWheel(ID):
	if ID >= 200 and ID < 300: #storm
		return 7.5
	elif ID >= 300 and ID < 600: #rain
		return 9.2
	elif ID >= 600 and ID < 700: #snow
		return 5.7
	elif (ID >= 700 and ID < 800) or (ID == 803 or ID == 804): #clouds
	     return 10.9
	elif ID == 800: #clear
		return 4.1
	elif ID == 801 or ID == 802: #partly cloudy
		return 2.6

# Determines number of LEDs to be lit up based on wind speed in mph
def mapLEDs(windspeed):
	if windspeed < 1:
		return 0
	elif windspeed >= 1 and windspeed < 7:
		return 1
	elif windspeed >= 7 and windspeed < 13:
		return 2
	elif windspeed >= 13 and windspeed < 22:
		return 3
	elif windspeed >= 22 and windspeed < 31:
		return 4
	elif windspeed >= 31 and windspeed < 45:
		return 5
	else:
		return 6

def rotate(p, old, new):
	change = 0.1
	
	if new == old:
		return
	elif new < old:
		change = -0.1

	while round(old, 1) != new:
		old = old + change
		p.ChangeDutyCycle(old)
		time.sleep(0.05)


