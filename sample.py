#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Sample script

"""
import temipy as temi


temi_serial = "01234567890"

# connect to the MQTT server
mqtt_client = temi.connect("test.mosquitto.org", 1883)

# create robot object
robot = temi.Robot(mqtt_client, "temi_serial")



command the robot to speak
robot.tts("Going to the Entrance")

command the robot to go to a saved location
robot.goto("entrance")


# play YouTube video by passing in a video ID
robot.youtube("ZsEano0qwcg")
time.sleep(10) # wait 10 seconds before performing next action


# tilt the robot's head to +55 degrees (absolute angle)
robot.tilt(+45)
time.sleep(3) # wait 3 seconds for action to complete

# tilt the robot's head to -15 degrees (absolute angle)
robot.tilt(-15)
time.sleep(3) # wait 3 seconds for action to complete

# tilt the robot's head to +30 degrees (relative angle)
robot.tilt_by(+30)
time.sleep(3) # wait 3 seconds for action to complete

# tilt the robot's head to -10 degrees (relative angle)
robot.tilt_by(-10)
time.sleep(3) # wait 3 seconds for action to complete


# rotate the robot by 90 degrees (relative angle)
robot.rotate(90)
time.sleep(5) # wait 5 seconds for action to complete

# rotate the robot by -30 degrees (relative angle)
robot.rotate(-30)
time.sleep(5) # wait 5 seconds for action to complete
