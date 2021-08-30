#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Sample script

"""
import pytemi as temi
import time


# parameters
MQTT_HOST = "test.mosquitto.org"
MQTT_PORT = 1883
TEMI_SERIAL = "01234567890"

# connect to the MQTT broker
mqtt_client = temi.connect(MQTT_HOST, MQTT_PORT)

# create robot object
robot = temi.Robot(mqtt_client, TEMI_SERIAL)


# --------------------------------------------------------------
# TEXT-TO-SPEECH COMMANDS
# --------------------------------------------------------------
robot.tts("Hello World!")  # command the robot to speak
time.sleep(1)  # wait some time for action to complete


# --------------------------------------------------------------
# WAYPOINT COMMANDS
# --------------------------------------------------------------
robot.goto("entrance")  # command the robot to go to a saved location
time.sleep(3)  # wait some time for action to complete


# --------------------------------------------------------------
# MOVE COMMANDS
# --------------------------------------------------------------
robot.tilt(+45)  # tilt the robot's head (absolute angle)
time.sleep(3)  # wait some time for action to complete

robot.tilt(-15)  # tilt the robot's head (absolute angle)
time.sleep(3)  # wait some time for action to complete

robot.tilt_by(+30)  # tilt the robot's head (relative angle)
time.sleep(3)  # wait some time for action to complete

robot.tilt_by(-10)  # tilt the robot's head (relative angle)
time.sleep(3)  # wait some time for action to complete

robot.rotate(90)  # rotate the robot (relative angle)
time.sleep(5)  # wait some time for action to complete

robot.rotate(-30)  # rotate the robot (relative angle)
time.sleep(5)  # wait some time for action to complete


# --------------------------------------------------------------
# MEDIA COMMANDS
# --------------------------------------------------------------
robot.video(
    "https://roboteam-assets.s3.eu-central-1.amazonaws.com/ui/skills/tutorials/videos/intorducing+temi.mp4"
)  # play online video by passing a URL; make sure video is optimized for the web (this sample video is not)
time.sleep(30)  # wait some time for action to complete

# show webview by passing a URL
robot.webview("https://www.google.com/")
time.sleep(5)
