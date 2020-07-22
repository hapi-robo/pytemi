#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""temi Robot Class


"""
import math
import json


class Robot:
    """Robot Class

    """

    def __init__(self, mqtt_client, temi_serial):
        """Constructor

        """
        self.client = mqtt_client
        self.serial = temi_serial

    def rotate(self, angle):
        """Rotate robot

        """
        print("[CMD] Rotate: {} [deg]".format(angle))

        topic = "temi/" + self.serial + "/command/move/turn_by"
        payload = json.dumps({"angle": angle})

        self.client.publish(topic, payload, qos=0)

    def translate(self, value):
        """Translate robot

        """
        print("[CMD] Translate: {} [unitless]".format(value))

        if math.copysign(1, value):
            topic = "temi/" + self.serial + "/command/move/forward"
        elif math.copysign(1, value):
            topic = "temi/" + self.serial + "/command/move/backward"
        else:
            pass  # do nothing

        self.client.publish(topic, "{}", qos=0)

    def tilt(self, angle):
        """Tilt robot's head (absolute angle)

        """
        print("[CMD] Tilt: {} [deg]".format(angle))

        topic = "temi/" + self.serial + "/command/move/tilt"
        payload = json.dumps({"angle": angle})

        self.client.publish(topic, payload, qos=0)

    def tilt_by(self, angle):
        """Tilt robot's head (relative angle)

        """
        print("[CMD] Tilt By: {} [deg]".format(angle))

        topic = "temi/" + self.serial + "/command/move/tilt_by"
        payload = json.dumps({"angle": angle})

        self.client.publish(topic, payload, qos=0)

    def stop(self):
        """Follow

        """
        print("[CMD] Stop")

        topic = "temi/" + self.serial + "/command/move/stop"

        self.client.publish(topic, "{}", qos=1)

    def goto(self, location_name):
        """Go to a specified location

        """
        print("[CMD] Go-To: {}".format(location_name))

        topic = "temi/" + self.serial + "/command/waypoint/goto"
        payload = json.dumps({"location": location_name})

        self.client.publish(topic, payload, qos=1)

    def tts(self, text):
        """Text-to-speech

        """
        print("[CMD] TTS: {}".format(text))

        topic = "temi/" + self.serial + "/command/tts"
        payload = json.dumps({"utterance": text})

        self.client.publish(topic, payload, qos=1)

    # def audio(self, url):
    #     """Play audio

    #     """
    #     print("[CMD] Play Audio: {}".format(url))

    #     topic = "temi/" + self.serial + "/command/media/audio"
    #     payload = json.dumps({"url": url})

    #     self.client.publish(topic, payload, qos=1)

    def video(self, url):
        """Play video

        """
        print("[CMD] Play Video: {}".format(url))

        topic = "temi/" + self.serial + "/command/media/video"
        payload = json.dumps({"url": url})

        self.client.publish(topic, payload, qos=1)

    def youtube(self, video_id):
        """Play YouTube

        """
        print("[CMD] Play YouTube: {}".format(video_id))

        topic = "temi/" + self.serial + "/command/media/youtube"
        payload = json.dumps({"video_id": video_id})

        self.client.publish(topic, payload, qos=1)

    def webview(self, url):
        """Show webview

        """
        print("[CMD] Show Webview: {}".format(url))

        topic = "temi/" + self.serial + "/command/media/webview"
        payload = json.dumps({"url": url})

        self.client.publish(topic, payload, qos=1)

    def call(self, room_name):
        """Start a call

        """
        print("[CMD] Call: {}".format(room_name))

        topic = "temi/" + self.serial + "/command/call/start"
        payload = json.dumps({"room_name": room_name})

        self.client.publish(topic, payload, qos=1)

    def hangup(self):
        """End a call

        """
        print("[CMD] Hangup")

        topic = "temi/" + self.serial + "/command/call/end"

        self.client.publish(topic, "{}", qos=1)
