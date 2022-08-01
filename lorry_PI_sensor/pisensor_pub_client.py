import json

import RPi.GPIO as GPIO
import time

import paho.mqtt.client as mqtt

import config

PIPin = 7


def on_connect(client, userdata, flags, rc):
    print("Connected with result code"+str(rc))


def on_publish(client, userdata, result):
    print("data published: %s\n", userdata)
    pass


def sensor_client_setup():
    sensor_client = mqtt.Client(config.CLIENT_ID)
    sensor_client.on_publish = on_publish
    sensor_client.connect(config.MQTT_BROKER, config.PORT)
    return sensor_client


def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(PIPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(PIPin,
                          GPIO.BOTH,
                          callback=detect,
                          bouncetime=200)


def pack_message(x):
    if x == 1:
        message_json = {
            "Result": True,
            "Timestamp": int(time.time())
        }
        message = json.dumps(message_json)
        print("published to MQTT broker:\nlorry has left loading bay: %s\n", message)
        topic = str.format("%s/%s", config.CLIENT_ID, config.SENSOR_ID)
        client_pub.publish(topic=topic, payload=message, qos=0)


def loop():
    while True:
        pass


def detect(chn):
    pack_message(GPIO.input(PIPin))


def destroy():
    GPIO.cleanup()


# start


client_pub = sensor_client_setup()
setup()
try:
    loop()
except KeyboardInterrupt:
    destroy()

