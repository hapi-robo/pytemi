#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Commands temi to randomly go to saved locations

"""
import pytemi as temi
import random
import csv
import os

from time import sleep
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()


# robot parameters
TEMI_SERIAL = "00119260058"

BATTERY_THRESHOLD_LOW = 20 # [%]
BATTERY_THRESHOLD_CHARGED = 90 # [%]

# MQTT server parameters
MQTT_HOST = os.getenv("MQTT_HOST")
MQTT_PORT = int(os.getenv("MQTT_PORT"))
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")


class bcolors:
    """ANSI escape sequences for colours"""

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def goto(robot, location):
    """Send robot to a location (blocking call)

    """
    robot.tts("Going to {}".format(location))
    robot.goto(location)
    sleep(2)

    # wait until goto-location is reached or is aborted
    while robot.goto_status != robot.GOTO_COMPLETE:
        print("[{}][{}][GOTO] {} [{}%]".format(
            datetime.now().strftime("%Y-%m-%d"),
            datetime.now().strftime("%H:%M:%S"), 
            robot.goto_status, 
            robot.battery))
        sleep(1)

        if robot.goto_status == robot.GOTO_ABORT:
            robot.tts("Go-To Aborted")
            sleep(1)
            print("{}{}[{}][{}][GOTO] Aborted ({}){}{}".format(
                        bcolors.BOLD,
                        bcolors.FAIL,
                        datetime.now().strftime("%Y-%m-%d"),
                        datetime.now().strftime("%H:%M:%S"),
                        location,
                        bcolors.ENDC,
                        bcolors.ENDC,))
            sleep(1)
            return -1

    # success
    return 0

def charge(robot):
    """Charge robot (blocking call)

    """
    robot.tts("Charging battery")
    while robot.battery < BATTERY_THRESHOLD_CHARGED:
        print("[{}][{}][CHARGING] Battery: {}%".format(
            datetime.now().strftime("%Y-%m-%d"),
            datetime.now().strftime("%H:%M:%S"),
            robot.battery))
        sleep(5 * 60)



if __name__ == "__main__":
    csv_filename = datetime.now().strftime("%Y%m%d_%H%M%S.csv")
    location_old = None

    # connect to the MQTT server
    mqtt_client = temi.connect(MQTT_HOST, MQTT_PORT, MQTT_USERNAME, MQTT_PASSWORD)

    # create robot object
    robot = temi.Robot(mqtt_client, TEMI_SERIAL)
    
    # collect locations
    while not robot.locations:
        print(robot.locations)
        sleep(1)
    locations = robot.locations 
    locations.pop(0) # remove "home base" from the list

    # start random patrol
    while True:
        # return robot to home base when battery is low
        if robot.battery < BATTERY_THRESHOLD_LOW:
            goto(robot, 'home base')
            charge(robot)

        # shuffle locations and go to each one
        random.shuffle(locations) # shuffle locations
        for location in locations:
            result = goto(robot, location)
            print("[{}][{}] {} → {} | {} [{}%]".format(
                datetime.now().strftime("%Y-%m-%d"),
                datetime.now().strftime("%H:%M:%S"),
                location_old,
                location,
                result,
                robot.battery))

            # collect logs and statistics
            with open(csv_filename, mode="a") as f:
                fieldnames = ["Date", "Time", "From", "To", "Result", "Battery"]
                csv_writer = csv.DictWriter(f, fieldnames=fieldnames)

                csv_writer.writerow({
                    'Date': datetime.now().strftime("%Y-%m-%d"), 
                    'Time': datetime.now().strftime("%H:%M:%S"), 
                    'From': location_old,
                    'To': location,
                    'Result': result,
                    'Battery': robot.battery
                    })

            # if robot reached the desired location, update old location
            if result == 0:
                location_old = location