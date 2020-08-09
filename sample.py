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

# connect to the MQTT server
mqtt_client = temi.connect(MQTT_HOST, MQTT_PORT)

# create robot object
robot = temi.Robot(mqtt_client, TEMI_SERIAL)


# --------------------------------------------------------------
# TEXT-TO-SPEECH COMMANDS
# --------------------------------------------------------------
robot.tts("Going to the Entrance")


# --------------------------------------------------------------
# WAYPOINT COMMANDS
# --------------------------------------------------------------
robot.goto("entrance")


# --------------------------------------------------------------
# MOVE COMMANDS
# --------------------------------------------------------------
robot.tilt(+45)
time.sleep(3)

robot.tilt(-15)
time.sleep(3)

robot.tilt_by(+30)
time.sleep(3)

robot.tilt_by(-10)
time.sleep(3)

robot.rotate(90)
time.sleep(5)

robot.rotate(-30)
time.sleep(5)


# --------------------------------------------------------------
# MEDIA COMMANDS
# --------------------------------------------------------------
# play YouTube video by passing in a video ID
robot.youtube("ZsEano0qwcg")
time.sleep(30)

# play online video by passing a URL
robot.video(
    "https://roboteam-assets.s3.eu-central-1.amazonaws.com/ui/skills/tutorials/videos/intorducing+temi.mp4"
)
time.sleep(30)

# show webview by passing a URL
robot.webview("https://www.robotemi.com/")
time.sleep(5)
robot.webview("https://www.his.co.jp/en/")
time.sleep(5)
robot.webview("https://hapi-robo.com/")
time.sleep(5)
