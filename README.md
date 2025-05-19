# 💡 Smart Lighting System

An intelligent home lighting system that operates automatically based on environmental conditions, such as motion and light level. The system includes simulated sensors, MQTT-based communication, logic-based decision making, a user-friendly GUI, and a local database for event logging.

---

## 📁 Project Structure

- emulator.py – Simulates motion and light sensors by publishing random values at intervals.
- manager.py – Processes incoming sensor data, applies the logic, controls the relay, and sends alerts.
- gui.py – Displays real-time sensor data, light status, and alerts using a graphical interface.
- data_acq.py – Manages the SQLite database that stores lighting events.
- init.py – Contains general configuration parameters such as broker IP, topics, thresholds, and DB path.
- data/smart_lighting.db – SQLite database file used for local storage.

---

## 🎯 Project Goal

To design and implement an energy-efficient, real-time smart lighting system using IoT principles.  
The system aims to:
- Turn lights on/off automatically based on motion and ambient light.
- Alert users of abnormal conditions (low light or no motion).
- Log events for future analysis.

---

## ⚙️ Technologies Used

- Python 3.x
- PyQt5 (GUI)
- paho-mqtt (MQTT client)
- SQLite (local database)
- Multithreading (for parallel sensor simulation)

---

## 🧠 System Logic

- Turn on the light if:
  - Motion is detected *and*
  - Light level is below *20*
- Trigger an alert if:
  - Light level drops below *10*
  - No motion is detected for *30 seconds*
- Once conditions return to normal, stop alerting and display a green status in the GUI.

---

## 🖥️ User Interface (GUI)

- Displays:
  - Current light level
  - Motion status
  - Light status (on/off)
  - Alerts (visual, color-coded)
- Real-time updates every second
- Simple and clean layout for user-friendly experience

---

## 🗃️ Database

- SQLite-based local DB located at data/smart_lighting.db
- Stores:
  - Timestamp
  - Light level
  - Motion detection state
  - Light on/off status
- Used for diagnostics, analysis, or tracking system performance

---

## 🚀 How to Run

1. *Start the emulator (sensor simulation):*
   bash
   python emulator.py
2. Start the manager (logic & control):
   bash
   python manager.py
3. Launch the graphical interface (GUI):
   ```bash
   python gui.py
