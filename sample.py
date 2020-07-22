#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Sample script

"""
import temipy as temi
import time


# parameters
MQTT_HOST = "test.mosquitto.org"
MQTT_PORT = 1883
TEMI_SERIAL = "01234567890"

# connect to the MQTT server
mqtt_client = temi.connect(MQTT_HOST, MQTT_PORT)

# create robot object
robot = temi.Robot(mqtt_client, TEMI_SERIAL)


# --------------------------------------------------------------
# TEXT-TO-SPEECH COMMANDS
# --------------------------------------------------------------
# command the robot to speak
robot.tts("Going to the Entrance")


# --------------------------------------------------------------
# WAYPOINT COMMANDS
# --------------------------------------------------------------
# command the robot to go to a saved location
robot.goto("entrance")


# --------------------------------------------------------------
# MOVE COMMANDS
# --------------------------------------------------------------
# tilt the robot's head to +55 degrees (absolute angle)
robot.tilt(+45)
time.sleep(3)  # wait 3 seconds for action to complete

# tilt the robot's head to -15 degrees (absolute angle)
robot.tilt(-15)
time.sleep(3)  # wait 3 seconds for action to complete

# tilt the robot's head to +30 degrees (relative angle)
robot.tilt_by(+30)
time.sleep(3)  # wait 3 seconds for action to complete

# tilt the robot's head to -10 degrees (relative angle)
robot.tilt_by(-10)
time.sleep(3)  # wait 3 seconds for action to complete

# rotate the robot by 90 degrees (relative angle)
robot.rotate(90)
time.sleep(5)  # wait 5 seconds for action to complete

# rotate the robot by -30 degrees (relative angle)
robot.rotate(-30)
time.sleep(5)  # wait 5 seconds for action to complete


# --------------------------------------------------------------
# MEDIA COMMANDS
# --------------------------------------------------------------
# play YouTube video by passing in a video ID
robot.youtube("ZsEano0qwcg")
time.sleep(30)  # wait 30 seconds before performing next action

# play online video by passing a URL
robot.video(
    "https://roboteam-assets.s3.eu-central-1.amazonaws.com/ui/skills/tutorials/videos/intorducing+temi.mp4"
)
time.sleep(30)  # wait 30 seconds before performing next action

# show webview by passing a URL
robot.webview("https://www.robotemi.com/")
time.sleep(5)  # wait 5 seconds before performing next action
robot.webview("https://www.his.co.jp/en/")
time.sleep(5)  # wait 5 seconds before performing next action
robot.webview("https://hapi-robo.com/")
time.sleep(5)  # wait 5 seconds before performing next action
