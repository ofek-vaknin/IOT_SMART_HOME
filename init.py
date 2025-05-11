# === init.py ===
import socket
import os

nb = 1  # 0 = local, 1 = HiveMQ
brokers = [
    str(socket.gethostbyname("localhost")),
    str(socket.gethostbyname("broker.hivemq.com"))
]
ports = ["1883", "1883"]
usernames = ["", ""]
passwords = ["", ""]

broker_ip = brokers[nb]
broker_port = ports[nb]
username = usernames[nb]
password = passwords[nb]

comm_topic = "pr/SmartLight/"

conn_time = 0
manag_time = 5
light_threshold = 40

# DB
db_name = os.path.join("data", "smart_lighting.db")
db_init = False