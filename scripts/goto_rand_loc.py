#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Temi randomly and continuously goes to any saved location

"""
import pytemi as temi
import time
import random


# parameters
MQTT_HOST = "test.mosquitto.org"
MQTT_PORT = 1883
TEMI_SERIAL = "01234567890"

# connect to the MQTT broker
mqtt_client = temi.connect(MQTT_HOST, MQTT_PORT)

# create robot object
robot = temi.Robot(mqtt_client, TEMI_SERIAL)

# --------------------------------------------------------------


# Go to random location

LOCATIONS = ["Kitchen", "Home Base", "Entrance", "Living room", "Kitchen"]

while True:
	robot.goto(random.choice(LOCATIONS)) # command the robot to go to a random saved location
	time.sleep(10) # wait some time for action to complete



