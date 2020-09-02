#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Sample script

"""
import pytemi as temi
import time
import random


# parameters
MQTT_HOST = "34.83.131.39"
MQTT_PORT = 1883
MQTT_USERNAME = "connect"
MQTT_PASSWORD = "hrstqa123"
TEMI_SERIAL = "00119260058"

# connect to the MQTT server
mqtt_client = temi.connect(MQTT_HOST, MQTT_PORT, MQTT_USERNAME, MQTT_PASSWORD)

# create robot object
robot = temi.Robot(mqtt_client, TEMI_SERIAL)

# --------------------------------------------------------------


# Go to random location

locations = ["Kitchen", "Home Base", "Entrance", "Living room", "Kitchen"]

while True:
	robot.goto(random.choice(locations)) # command the robot to go to a random saved location
	time.sleep(10) # wait some time for action to complete



