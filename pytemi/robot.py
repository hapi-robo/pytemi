#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""temi Robot Class

"""
import math
import json

from datetime import datetime


def now():
    """Return time in string format"""
    return datetime.now().strftime("%H:%M:%S")


def _on_status(client, userdata, msg):
    d = json.loads(msg.payload)
    userdata["locations"] = d["waypoint_list"]
    userdata["battery"]["percentage"] = d["battery_percentage"]


def _on_battery(client, userdata, msg):
    print("[{}] [SUB] [BATTERY] {}".format(now(), str(msg.payload)))
    d = json.loads(msg.payload)
    userdata["battery"]["percentage"] = d["percentage"]
    userdata["battery"]["is_charging"] = d["is_charging"]


def _on_goto(client, userdata, msg):
    d = json.loads(msg.payload)
    userdata["goto"]["location"] = d["location"]
    userdata["goto"]["status"] = d["status"]


def _on_user(client, userdata, msg):
    print("[{}] [SUB] [USER] {}".format(now(), str(msg.payload)))
    userdata["user"] = json.loads(msg.payload)


class Robot:
    """Robot Class"""

    def __init__(self, mqtt_client, temi_serial, silent=True):
        """Constructor"""
        self.client = mqtt_client
        self.id = temi_serial
        self.silent = silent

        # set user data
        self.state = {"locations": [], "battery": {}, "goto": {}, "user": {}}
        self.client.user_data_set(self.state)

        # attach subscription callbacks
        self.client.message_callback_add(
            "temi/{}/status/info".format(temi_serial), _on_status
        )
        self.client.message_callback_add(
            "temi/{}/status/utils/battery".format(temi_serial), _on_battery
        )
        self.client.message_callback_add(
            "temi/{}/event/waypoint/goto".format(temi_serial), _on_goto
        )
        self.client.message_callback_add(
            "temi/{}/event/user/detection".format(temi_serial), _on_user
        )

    def rotate(self, angle):
        """Rotate"""
        if not self.silent:
            print("[CMD] Rotate: {} [deg]".format(angle))

        if angle != 0:
            topic = "temi/" + self.id + "/command/move/turn_by"
            payload = json.dumps({"angle": angle})

            self.client.publish(topic, payload, qos=0)

    def joystick(self, x, y):
        """Joystick"""
        if not self.silent:
            print("[CMD] Translate: {} {} [unitless]".format(x, y))

        topic = "temi/" + self.id + "/command/move/joystick"
        payload = json.dumps({"x": x, "y": y})

        self.client.publish(topic, payload, qos=0)

    def tilt(self, angle):
        """Tilt head (absolute angle)"""
        if not self.silent:
            print("[CMD] Tilt: {} [deg]".format(angle))

        topic = "temi/" + self.id + "/command/move/tilt"
        payload = json.dumps({"angle": angle})

        self.client.publish(topic, payload, qos=0)

    def tilt_by(self, angle):
        """Tilt head (relative angle)"""
        if not self.silent:
            print("[CMD] Tilt By: {} [deg]".format(angle))

        topic = "temi/" + self.id + "/command/move/tilt_by"
        payload = json.dumps({"angle": angle})

        self.client.publish(topic, payload, qos=0)

    def stop(self):
        """Stop"""
        if not self.silent:
            print("[CMD] Stop")

        topic = "temi/" + self.id + "/command/move/stop"

        self.client.publish(topic, "{}", qos=1)

    def follow(self):
        """Follow"""
        if not self.silent:
            print("[CMD] Follow")

        topic = "temi/" + self.id + "/command/follow/unconstrained"

        self.client.publish(topic, "{}", qos=1)

    def goto(self, location_name):
        """Go to a saved location"""
        if not self.silent:
            print("[CMD] Go-To: {}".format(location_name))

        topic = "temi/" + self.id + "/command/waypoint/goto"
        payload = json.dumps({"location": location_name})

        self.client.publish(topic, payload, qos=1)

    def tts(self, text):
        """Text-to-speech"""
        if not self.silent:
            print("[CMD] TTS: {}".format(text))

        topic = "temi/" + self.id + "/command/tts"
        payload = json.dumps({"utterance": text})

        self.client.publish(topic, payload, qos=1)

    def video(self, url):
        """Play video"""
        if not self.silent:
            print("[CMD] Play Video: {}".format(url))

        topic = "temi/" + self.id + "/command/media/video"
        payload = json.dumps({"url": url})

        self.client.publish(topic, payload, qos=1)

    def webview(self, url):
        """Show webview"""
        if not self.silent:
            print("[CMD] Show Webview: {}".format(url))

        topic = "temi/" + self.id + "/command/media/webview"
        payload = json.dumps({"url": url})

        self.client.publish(topic, payload, qos=1)

    def custom(self, topic, data):
        """Send custom message"""
        if not self.silent:
            print("[CMD] Custom")

        topic = "temi/" + self.id + topic
        payload = json.dumps(data)

        self.client.publish(topic, payload, qos=1)

    @property
    def locations(self):
        """Return a list of locations"""
        if "locations" in self.state:
            return self.state["locations"]
        else:
            return []

    @property
    def goto_status(self):
        if "status" in self.state["goto"]:
            return self.state["goto"]["status"]
        else:
            return None

    @property
    def battery(self):
        return self.state["battery"]["percentage"]

    @property
    def GOTO_START(self):
        return "start"

    @property
    def GOTO_ABORT(self):
        return "abort"

    @property
    def GOTO_GOING(self):
        return "going"

    @property
    def GOTO_COMPLETE(self):
        return "complete"

    @property
    def GOTO_CALCULATING(self):
        return "calculating"

    @property
    def GOTO_OBSTACLE(self):
        return "obstacle detected"
