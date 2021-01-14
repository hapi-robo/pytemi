#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Commands temi by joystick

"""
import pytemi as temi
import time
import threading
import concurrent.futures
import copy
import inputs
import os

from dotenv import load_dotenv
load_dotenv()


# robot parameters
# TEMI_SERIAL = "00119260058" # tony
TEMI_SERIAL = "00119140088" # gary

# MQTT server parameters
MQTT_HOST = os.getenv("MQTT_HOST")
MQTT_PORT = int(os.getenv("MQTT_PORT"))
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

# control
PUBLISH_INTERVAL = 0.1 # [sec]
ANGULAR_VELOCITY = 30 # [deg/s]

# robot limits
TILT_ANGLE_MAX_POS = 55 # [deg]
TILT_ANGLE_MAX_NEG = -20 # [deg]
ANGULAR_VELOCITY_MIN = 0.3 # [normalized]
LINEAR_VELOCITY_MIN = 0.5 # [normalized]


class Pipeline:
    """Single element pipeline between producer and consumer
    
    """
    def __init__(self):
        self._message = {}
        self._lock = threading.Lock()

    def get_message(self):
        if self._lock.acquire(blocking=False):
            message = copy.deepcopy(self._message)
            self._lock.release()
        
        return message

    def set_message(self, message):
        if self._lock.acquire(blocking=False):
            self._message = copy.deepcopy(message)
            self._lock.release()


def publisher(pipeline):
    """Robot publisher thread

    """
    tilt_angle = 0
    linear_velocity = 0.0
    angular_velocity = 0.0

    while True:
        cmd = pipeline.get_message()

        # translate
        if 'abs_y' in cmd:
            # reverse axis
            linear_velocity = -cmd['abs_y']

            # check for minimum linear velocity
            if abs(linear_velocity) > LINEAR_VELOCITY_MIN:
                robot.translate(linear_velocity)

        # rotate
        if 'abs_x' in cmd:
            # reverse axis
            angular_velocity = -cmd['abs_x']
        
            # check for minimum angular velocity
            if abs(angular_velocity) > ANGULAR_VELOCITY_MIN:
                if angular_velocity > 0:
                    robot.rotate(+ANGULAR_VELOCITY)
                elif angular_velocity < 0:
                    robot.rotate(-ANGULAR_VELOCITY)
                else:
                    pass

        # tilt
        if 'abs_ry' in cmd:
            # scale tilt-angle
            if cmd['abs_ry'] > 0:
                tilt_angle = +int(TILT_ANGLE_MAX_POS * cmd['abs_ry'])
            elif cmd['abs_ry'] < 0:
                tilt_angle = -int(TILT_ANGLE_MAX_NEG * cmd['abs_ry'])
            else:
                tilt_angle = 0

            if abs(tilt_angle) > 0:
                robot.tilt_by(tilt_angle)


        # print to console
        print("--------------------")
        print("Timestamp: {:.2f}".format(time.time()))
        print("Translate: {:+.2f}".format(linear_velocity))
        print("Rotate: {:+.2f}".format(angular_velocity))
        print("Tilt: {:+}".format(tilt_angle))

        # wait
        time.sleep(PUBLISH_INTERVAL)


def subscriber(pipeline):
    """Joystick subscriber thread

    """
    cmd = {}

    while True:
        # clear command
        cmd.clear()

        # collect gamepad events (blocking)
        events = inputs.get_gamepad()
        
        # parse all events
        for event in events:
            if event.ev_type is not "Sync":
                # print("{} {} {}".format(event.ev_type, event.code, event.state))
                
                val_norm = event.state / 32768.0

                if event.code is "ABS_Y":
                    cmd['abs_y'] = val_norm

                if event.code is "ABS_X":
                    cmd['abs_x'] = val_norm

                if event.code is "ABS_RY":
                    cmd['abs_ry'] = val_norm


        if cmd:
            # print(cmd)
            pipeline.set_message(cmd)


if __name__ == "__main__":
    # connect to the MQTT server
    mqtt_client = temi.connect(MQTT_HOST, MQTT_PORT, MQTT_USERNAME, MQTT_PASSWORD)

    # create robot object
    robot = temi.Robot(mqtt_client, TEMI_SERIAL)
    
    # verify joystick connection
    if len(inputs.devices.gamepads) == 0:
        raise Exception("Could not find any gamepads")

    # construct pipeline
    pipeline = Pipeline()

    # start threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(subscriber, pipeline)
        executor.submit(publisher, pipeline)