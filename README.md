# temi Connect Python Package
Control temi using Python scripts over MQTT.


## Prerequisites
* [Python 3](https://www.python.org/downloads/)
* Python [virtualenv](https://virtualenv.pypa.io/en/stable/installation.html)
* Connect APK installed on temi, see [here](https://github.com/hapi-robo/connect)
* MQTT broker. Free brokers for testing:
	* [Eclipse](http://test.mosquitto.org/)
	* [Mosquitto](http://mqtt.eclipse.org)
	* [HiveMQ](http://broker.hivemq.com)


## Ubuntu/MacOS Setup
Clone this repository:
```
git clone ...
```

Create a Python virtual environment (`venv`) and install all dependencies:
```
cd temipy/
./setup.sh
```

To activate the virtual environment:
```
source venv/bin/activate
```


## Usage
Make sure temi is connected to an MQTT broker via the Connect app.

Example:
```
import temipy as temi

temi_serial = "01234567890"

# connect to the MQTT server
mqtt_client = temi.connect("test.mosquitto.org", 1883)

# create robot object
robot = temi.Robot(mqtt_client, "temi_serial")

# command the robot to speak
robot.tts("Going to the Entrance")

# command the robot to go to a saved location
robot.goto("entrance")
```

See `sample.py` for more details.
