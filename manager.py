# === manager.py ===
import paho.mqtt.client as mqtt
import time
from init import *
import sqlite3
from datetime import datetime

# Internal state
light_level = 100
motion_detected = False
relay_state = False
last_motion_time = time.time()
alarm_sent_low_light = False
alarm_sent_no_motion = False
normal_state_sent = False  # כדי לשלוח רק פעם אחת שהכל חזר לתקין

def save_to_db(light, motion, relay):
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS lighting_events (
        timestamp TEXT,
        light_level INTEGER,
        motion_detected INTEGER,
        light_on INTEGER
    )''')
    c.execute("INSERT INTO lighting_events VALUES (?, ?, ?, ?)",
              (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), light, int(motion), int(relay)))
    conn.commit()
    conn.close()

def process():
    global relay_state, alarm_sent_low_light, alarm_sent_no_motion, normal_state_sent

    now = time.time()

    # ==== Control light ====
    if motion_detected and light_level < 20:
        new_state = True
    elif light_level < 20:
        new_state = True
    else:
        new_state = False

    if new_state != relay_state:
        relay_state = new_state
        print("[MANAGER] Relay changed to:", "ON" if relay_state else "OFF")
        client.publish(comm_topic + "relay", f"Relay:{int(relay_state)}")
        save_to_db(light_level, motion_detected, relay_state)

    # ==== Alarms ====
    low_light_alarm = light_level < 10
    no_motion_alarm = (now - last_motion_time) > 30

    if low_light_alarm and not alarm_sent_low_light:
        client.publish(comm_topic + "alarm", "Very low light detected (<10)")
        alarm_sent_low_light = True
        normal_state_sent = False
    elif not low_light_alarm:
        alarm_sent_low_light = False

    if no_motion_alarm and not alarm_sent_no_motion:
        client.publish(comm_topic + "alarm", "No motion detected for 30 seconds")
        alarm_sent_no_motion = True
        normal_state_sent = False
    elif not no_motion_alarm:
        alarm_sent_no_motion = False

    if not low_light_alarm and not no_motion_alarm and not normal_state_sent:
        client.publish(comm_topic + "normal", "All conditions normal")
        normal_state_sent = True

def on_message(client, userdata, msg):
    global light_level, motion_detected, last_motion_time
    payload = msg.payload.decode("utf-8")
    topic = msg.topic

    if "light" in topic:
        light_level = int(payload.split(":")[1])
    elif "motion" in topic:
        motion_detected = payload.split(":")[1] == '1'
        if motion_detected:
            last_motion_time = time.time()

    process()

def on_connect(client, userdata, flags, rc):
    print("[MANAGER] Connected with result code " + str(rc))
    client.subscribe(comm_topic + "#")

client = mqtt.Client("Manager")
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_ip, int(broker_port), 60)
client.loop_forever()