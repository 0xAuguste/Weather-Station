# Weather Station Server

#Flask stuff
from flask import Flask
app = Flask(__name__)

#DHT11 Setup
import time
import board
import adafruit_dht
 
# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT11(board.D18)

@app.route('/')
def hello_world():
    return 'Hello, World! Temp and Humidity Homepage.'

@app.route('/temp')
def get_temp():
    while True:
        try:
            temperature = dhtDevice.temperature
            break
        except RuntimeError as error:
            time.sleep(2)
        except Exception as error:
            dhtDevice.exit()
            raise error
            break

    tempF = temperature * (9/5) + 32
    return 'Temperature: %f'%tempF

@app.route('/humid')
def get_humid():
    while True:
        try:
            humid = dhtDevice.humidity
            break
        except RuntimeError as error:
            time.sleep(2)
        except Exception as error:
            dhtDevice.exit()
            raise error
            break

    return 'Humidity: %f'%humid
