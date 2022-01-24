# Runs weather station electromechanical art installation
# Function definitions are in helperfuncs.py
# Written by Auguste Brown

import RPi.GPIO as GPIO
import time
import tm1637
from helperfuncs import *

server_IP = 'https://debee29c4aab.ngrok.io' #IP address of RPi in Vermont
API_URL = 'http://api.openweathermap.org/data/2.5/weather?id=5238755&units=imperial&APPID='

servo_pin = 12 #GPIO pin 12 (has hardware PWM)
LED_pins = [17, 27, 22, 10, 9, 11]

# Setup GPIO and assign ouput pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)
for pin in LED_pins:
	GPIO.setup(pin, GPIO.OUT)
pulse = GPIO.PWM(servo_pin, 50) #setup servo PWM at 50 Hz

# Create object for display:
# TM1637 wiring: CLK -> GPIO #3; DIO -> GPIO #4; VCC -> 5V (pin 2)
display = tm1637.TM1637(clk=3, dio=4)
display.brightness(2)

# MAIN LOOP:
pulse.start(2.5) #start servo PWM
try:
	wheel_loc = 2.5
	while True:
		# Get data:
		current = queryAPI(API_URL) #request API data
		temp_reply = requests.get(server_IP + '/temp') #request sensor data from server in Vermont
		sensor_temp = int(round(float(temp_reply.text[13:]))) #convert from string to int

		# Map data to appropriate actuator state:
		old_wheel_loc = wheel_loc
		wheel_loc = mapWheel(current['cond_ID'])
		num_LEDs = mapLEDs(current['windspeed'])
		# Update actuator state:
		display.number(sensor_temp) #show temp on display
		for i in range(6): #turn appropriate LEDs on
			if i < num_LEDs:
				GPIO.output(LED_pins[i], GPIO.HIGH)
			else:
				GPIO.output(LED_pins[i], GPIO.LOW)
		rotate(pulse, old_wheel_loc, wheel_loc) #rotate servo

		print('Description: ' + current['cond'])
		print('API Temperature: ' + str(current['temp']))
		print('Wind Speed: ' + str(current['windspeed']))
		print('Wheel Location: ' + str(wheel_loc))
		print('Num LEDs: ' + str(num_LEDs))
		print('')
		time.sleep(60)

except KeyboardInterrupt:
	rotate(pulse, wheel_loc, 2.5) #return servo
	pulse.stop()
	GPIO.cleanup()
	display.show('    ') #turn display off
