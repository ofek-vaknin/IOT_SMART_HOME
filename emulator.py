# === emulator.py ===
import random
import time
import paho.mqtt.client as mqtt
from init import *
from threading import Thread

class LightSensorEmulator(Thread):
    def __init__(self, client, topic, interval=5):
        super().__init__()
        self.client = client
        self.topic = topic
        self.interval = interval
        self.running = True

    def run(self):
        while self.running:
            level = random.randint(0, 100)
            message = f"Light:{level}"
            print(message)
            self.client.publish(self.topic, message)
            time.sleep(self.interval)

class MotionSensorEmulator(Thread):
    def __init__(self, client, topic, interval=7):
        super().__init__()
        self.client = client
        self.topic = topic
        self.interval = interval
        self.running = True

    def run(self):
        while self.running:
            state = random.choice(["Motion:1", "Motion:0"])
            print(state)
            self.client.publish(self.topic, state)
            time.sleep(self.interval)

class RelayEmulator:
    def __init__(self):
        self.state = False  # False = OFF, True = ON

    def set_state(self, on):
        self.state = on
        print("Relay ON" if self.state else "Relay OFF")


def init_emulator():
    client = mqtt.Client(client_id="Emulator", protocol=mqtt.MQTTv311)
    client.connect(broker_ip, int(broker_port))
    client.loop_start()

    light_sensor = LightSensorEmulator(client, comm_topic + "light")
    motion_sensor = MotionSensorEmulator(client, comm_topic + "motion")

    light_sensor.start()
    motion_sensor.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        light_sensor.running = False
        motion_sensor.running = False
        light_sensor.join()
        motion_sensor.join()
        client.loop_stop()


if __name__ == "__main__":
    init_emulator()