import random

from pirsensor import PIRSensor
from datetime import datetime
import credentials
from paho.mqtt import client as mqtt_client

broker = 'broker.emqx.io'
port = 1883

topic = "python/mqtt/motionTestData"

client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'emqx'
password = 'public'


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    pir_sensor = PIRSensor()
    while True:
        pir_sensor.set_up()
        pir_sensor.listen()
        motion_stamp = pir_sensor.package(datetime.now(), client_id)
        result = client.publish(topic, motion_stamp)
        if result[0] == 0:
            print(f"Send {motion_stamp} to topic {topic}")
        else:
            print(f"failed to send message to topic {topic}")


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()
