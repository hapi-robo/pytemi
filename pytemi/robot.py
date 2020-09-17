#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""temi Robot Class


"""
import math
import json

from datetime import datetime

def now():
    """Return time in string format

    """
    return datetime.now().strftime("%H:%M:%S")


def _on_status(client, userdata, msg):
    d = json.loads(msg.payload)
    userdata['locations'] = d['waypoint_list']
    userdata['battery']['percentage'] = d['battery_percentage']

def _on_battery(client, userdata, msg):
    print("[{}] [SUB] [BATTERY] {}".format(now(), str(msg.payload)))
    d = json.loads(msg.payload)
    userdata['battery']['percentage'] = d['percentage']
    userdata['battery']['is_charging'] = d['is_charging']

def _on_goto(client, userdata, msg):
    d = json.loads(msg.payload)
    userdata['goto']['location'] = d['location']
    userdata['goto']['status'] = d['status']

def _on_user(client, userdata, msg):
    print("[{}] [SUB] [USER] {}".format(now(), str(msg.payload)))
    userdata['user'] = json.loads(msg.payload)


class Robot:
    """Robot Class

    """

    def __init__(self, mqtt_client, temi_serial):
        """Constructor

        """
        self.client = mqtt_client
        self.id = temi_serial

        # set user data
        self.state = { 
            'locations': [],
            'battery': {},
            'goto': {},
            'user': {}
        }
        self.client.user_data_set(self.state)
        
        # attach subscription callbacks
        self.client.message_callback_add("temi/{}/status/info".format(temi_serial), _on_status)
        # self.client.message_callback_add("temi/{}/status/utils/battery".format(temi_serial), _on_battery)
        self.client.message_callback_add("temi/{}/event/waypoint/goto".format(temi_serial), _on_goto)
        # self.client.message_callback_add("temi/{}/event/user/detection".format(temi_serial), _on_user)


    def rotate(self, angle):
        """Rotate

        """
        print("[CMD] Rotate: {} [deg]".format(angle))

        if (angle != 0):
            topic = "temi/" + self.id + "/command/move/turn_by"
            payload = json.dumps({"angle": angle})

            self.client.publish(topic, payload, qos=0)


    def translate(self, value):
        """Translate

        """
        print("[CMD] Translate: {} [unitless]".format(value))

        topic = "temi/" + self.id + "/command/move/joystick"
        payload = json.dumps({"x": value, "y": 0})

        self.client.publish(topic, payload, qos=0)


    # def translate(self, value):
    #     """Translate

    #     """
    #     print("[CMD] Translate: {} [unitless]".format(value))

    #     if math.copysign(1, value) > 0:
    #         topic = "temi/" + self.id + "/command/move/forward"
    #         self.client.publish(topic, "{}", qos=0)
    #     elif math.copysign(1, value) < 0:
    #         topic = "temi/" + self.id + "/command/move/backward"
    #         self.client.publish(topic, "{}", qos=0)
    #     else:
    #         pass  # do nothing


    def tilt(self, angle):
        """Tilt head (absolute angle)

        """
        print("[CMD] Tilt: {} [deg]".format(angle))

        topic = "temi/" + self.id + "/command/move/tilt"
        payload = json.dumps({"angle": angle})

        self.client.publish(topic, payload, qos=0)

    def tilt_by(self, angle):
        """Tilt head (relative angle)

        """
        print("[CMD] Tilt By: {} [deg]".format(angle))

        topic = "temi/" + self.id + "/command/move/tilt_by"
        payload = json.dumps({"angle": angle})

        self.client.publish(topic, payload, qos=0)

    def stop(self):
        """Stop

        """
        print("[CMD] Stop")

        topic = "temi/" + self.id + "/command/move/stop"

        self.client.publish(topic, "{}", qos=1)

    def follow(self):
        """Follow

        """
        print("[CMD] Follow")

        topic = "temi/" + self.id + "/command/follow/unconstrained"

        self.client.publish(topic, "{}", qos=1)

    def goto(self, location_name):
        """Go to a saved location

        """
        print("[CMD] Go-To: {}".format(location_name))

        topic = "temi/" + self.id + "/command/waypoint/goto"
        payload = json.dumps({"location": location_name})

        self.client.publish(topic, payload, qos=1)

    def tts(self, text):
        """Text-to-speech

        """
        print("[CMD] TTS: {}".format(text))

        topic = "temi/" + self.id + "/command/tts"
        payload = json.dumps({"utterance": text})

        self.client.publish(topic, payload, qos=1)

    # def audio(self, url):
    #     """Play audio

    #     """
    #     print("[CMD] Play Audio: {}".format(url))

    #     topic = "temi/" + self.id + "/command/media/audio"
    #     payload = json.dumps({"url": url})

    #     self.client.publish(topic, payload, qos=1)

    def video(self, url):
        """Play video

        """
        print("[CMD] Play Video: {}".format(url))

        topic = "temi/" + self.id + "/command/media/video"
        payload = json.dumps({"url": url})

        self.client.publish(topic, payload, qos=1)

    def youtube(self, video_id):
        """Play YouTube

        """
        print("[CMD] Play YouTube: {}".format(video_id))

        topic = "temi/" + self.id + "/command/media/youtube"
        payload = json.dumps({"video_id": video_id})

        self.client.publish(topic, payload, qos=1)

    def webview(self, url):
        """Show webview

        """
        print("[CMD] Show Webview: {}".format(url))

        topic = "temi/" + self.id + "/command/media/webview"
        payload = json.dumps({"url": url})

        self.client.publish(topic, payload, qos=1)

    def app(self, package_name):
        """Start Android app

        """
        print("[CMD] Start App: {}".format(package_name))

        topic = "temi/" + self.id + "/command/app"
        payload = json.dumps({"package_name": package_name})

        self.client.publish(topic, payload, qos=1)

    # def call(self, room_name):
    #     """Start a call

    #     """
    #     print("[CMD] Call: {}".format(room_name))

    #     topic = "temi/" + self.id + "/command/call/start"
    #     payload = json.dumps({"room_name": room_name})

    #     self.client.publish(topic, payload, qos=1)

    # def hangup(self):
    #     """End a call

    #     """
    #     print("[CMD] Hangup")

    #     topic = "temi/" + self.id + "/command/call/end"

    #     self.client.publish(topic, "{}", qos=1)

    @property
    def locations(self):
        """Return a list of locations

        """
        if 'locations' in self.state:
            return self.state['locations']
        else:
            return []

    @property
    def goto_status(self):
        if 'status' in self.state['goto']:
            return self.state['goto']['status']
        else:
            return None

    @property
    def battery(self):
        return self.state['battery']['percentage']
    
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
