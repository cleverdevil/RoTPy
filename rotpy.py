#!/usr/bin/env python3
import serial
import sys
import re
import json
import requests
from pathlib import Path

# Load configuration
CONFIG_PATH = Path(__file__).parent / "config.json"


def load_config():
    if not CONFIG_PATH.exists():
        print(f"Error: Configuration file not found at {CONFIG_PATH}")
        print("Creating a sample config.json...")
        sample = {
            "endpoint": "http://localhost:8080/api/orientation",
            "sensor_id": "display-1",
        }
        with open(CONFIG_PATH, "w") as f:
            json.dump(sample, f, indent=2)
        print(f"Please edit {CONFIG_PATH} and restart.")
        sys.exit(1)

    with open(CONFIG_PATH) as f:
        return json.load(f)


config = load_config()
ENDPOINT = config["endpoint"]
SENSOR_ID = config["sensor_id"]

port = sys.argv[1] if len(sys.argv) > 1 else "/dev/ttyACM0"

# Orientation states
LANDSCAPE = "LANDSCAPE"
PORTRAIT = "PORTRAIT"
PORTRAIT_FLIP = "PORTRAIT_FLIP"
LANDSCAPE_FLIP = "LANDSCAPE_FLIP"

current_orientation = None


def classify_orientation(pitch, roll):
    if abs(roll) < 45:
        if pitch < -45:
            return LANDSCAPE_FLIP
        else:
            return LANDSCAPE
    elif roll >= 45:
        return PORTRAIT
    elif roll <= -45:
        return PORTRAIT_FLIP

    return None


def notify_server(old_orientation, new_orientation):
    payload = {
        "sensor_id": SENSOR_ID,
        "from": old_orientation,
        "to": new_orientation,
    }

    try:
        response = requests.post(
            ENDPOINT,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=5,
        )
        response.raise_for_status()
        print("  -> Server notified successfully")
    except requests.RequestException as e:
        print(f"  -> Failed to notify server: {e}")


def main():
    global current_orientation

    print(f"Sensor ID: {SENSOR_ID}")
    print(f"Endpoint:  {ENDPOINT}")
    print(f"Serial:    {port}")
    print()

    pattern = re.compile(r"pitch=\s*([-\d.]+)\s+roll=\s*([-\d.]+)")

    with serial.Serial(port, 115200) as ser:
        while True:
            line = ser.readline().decode("utf-8", errors="ignore").strip()

            if not line:
                continue

            match = pattern.match(line)
            if match:
                pitch = float(match.group(1))
                roll = float(match.group(2))

                orientation = classify_orientation(pitch, roll)

                if orientation and orientation != current_orientation:
                    old = current_orientation or "UNKNOWN"
                    print(f"{old} -> {orientation}")
                    notify_server(old, orientation)
                    current_orientation = orientation


if __name__ == "__main__":
    main()
