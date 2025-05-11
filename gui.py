import sys
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QMainWindow, QTextEdit
from PyQt5.QtCore import QTimer
import paho.mqtt.client as mqtt
from init import *

# State variables
light_level = 0
motion_status = False
relay_status = False
last_alarm = ""

class SmartLightGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("💡 Smart Lighting Dashboard")
        self.setGeometry(300, 200, 400, 300)

        self.label_light = QLabel("🔆 Light Level: ...")
        self.label_motion = QLabel("🚶 Motion: ...")
        self.label_relay = QLabel("💡 Light Status: ...")
        self.label_light.setStyleSheet("font-size: 16px;")
        self.label_motion.setStyleSheet("font-size: 16px;")
        self.label_relay.setStyleSheet("font-size: 16px;")

        self.alert_box = QTextEdit()
        self.alert_box.setReadOnly(True)
        self.alert_box.setStyleSheet("background-color: #fff8dc; font-size: 14px; border: 1px solid gray;")

        layout = QVBoxLayout()
        layout.addWidget(self.label_light)
        layout.addWidget(self.label_motion)
        layout.addWidget(self.label_relay)
        layout.addWidget(QLabel("🔔 Alerts:"))
        layout.addWidget(self.alert_box)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Timer for GUI refresh
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_labels)
        self.timer.start(1000)

    def update_labels(self):
        self.label_light.setText(f"🔆 Light Level: {light_level}")
        self.label_motion.setText(f"🚶 Motion: {'Detected' if motion_status else 'None'}")
        self.label_relay.setText(f"💡 Light Status: {'ON' if relay_status else 'OFF'}")
        self.alert_box.setText(last_alarm)

# MQTT callbacks
def on_message(client, userdata, msg):
    global light_level, motion_status, relay_status, last_alarm
    payload = msg.payload.decode("utf-8")
    topic = msg.topic

    if "light" in topic:
        light_level = int(payload.split(":")[1])
    elif "motion" in topic:
        motion_status = payload.split(":")[1] == '1'
    elif "relay" in topic:
        relay_status = payload.split(":")[1] == '1'
    elif "alarm" in topic:
        last_alarm = f"⚠️ Alarm: {payload}"
    elif "normal" in topic:
        last_alarm = f"✅ {payload}"

def run_gui():
    client = mqtt.Client("GUI")
    client.on_message = on_message
    client.connect(broker_ip, int(broker_port))
    client.subscribe(comm_topic + "#")
    client.loop_start()

    app = QApplication(sys.argv)
    window = SmartLightGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run_gui()