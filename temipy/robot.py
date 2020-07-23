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
        self.id = temi_serial

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

        if math.copysign(1, value) > 0:
            topic = "temi/" + self.id + "/command/move/forward"
            self.client.publish(topic, "{}", qos=0)
        elif math.copysign(1, value) < 0:
            topic = "temi/" + self.id + "/command/move/backward"
            self.client.publish(topic, "{}", qos=0)
        else:
            pass  # do nothing


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

    def call(self, room_name):
        """Start a call

        """
        print("[CMD] Call: {}".format(room_name))

        topic = "temi/" + self.id + "/command/call/start"
        payload = json.dumps({"room_name": room_name})

        self.client.publish(topic, payload, qos=1)

    def hangup(self):
        """End a call

        """
        print("[CMD] Hangup")

        topic = "temi/" + self.id + "/command/call/end"

        self.client.publish(topic, "{}", qos=1)
