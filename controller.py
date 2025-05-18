import serial
import time
import json
import cv2

CONFIG_FILE = "config.json"
SERIAL_PORT = 'COM3'  # Update with your Arduino COM port
BAUD_RATE = 9600
LED_PIN = 9  # Arduino LED pin

def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {
            "mode": "motion",
            "minutes": 1,
            "start_action": "dim",
            "motion_action": "on",
            "end_action": "dim"  # this won't be used in motion mode now
        }

def send_command(ser, command):
    ser.write(f"{command}\n".encode())
    print(f"Sent command: {command}")

def main():
    config = load_config()
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    time.sleep(2)  # wait for Arduino to reset

    cap = cv2.VideoCapture(0)

    prev_frame = None
    motion_cooldown = 7  # seconds
    last_motion_time = 0
    led_state = config["start_action"]
    send_command(ser, led_state.upper())

    print(f"Starting with LED {led_state.upper()}")

    def motion_detected(curr_frame, prev_frame):
        gray1 = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(gray1, gray2)
        _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
        count = cv2.countNonZero(thresh)
        return count > 5000  # adjust sensitivity

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to read from camera")
            break

        if prev_frame is None:
            prev_frame = frame
            continue

        curr_time = time.time()

        if config["mode"] == "time":
            if led_state != config["start_action"]:
                send_command(ser, config["start_action"].upper())
                led_state = config["start_action"]
                start_time = curr_time

            if curr_time - start_time >= config["minutes"] * 60:
                if led_state != config["end_action"]:
                    send_command(ser, config["end_action"].upper())
                    led_state = config["end_action"]
            time.sleep(1)
            continue

        # Motion mode
        if motion_detected(frame, prev_frame):
            if curr_time - last_motion_time > motion_cooldown:
                send_command(ser, config["motion_action"].upper())
                led_state = config["motion_action"]
                last_motion_time = curr_time
                print(f"Motion detected - LED {led_state.upper()}")
        else:
            # Revert to whatever start_action is
            if led_state == config["motion_action"] and curr_time - last_motion_time > motion_cooldown:
                send_command(ser, config["start_action"].upper())
                led_state = config["start_action"]
                print(f"No motion - LED {led_state.upper()}")

        prev_frame = frame
        time.sleep(0.1)

if __name__ == "__main__":
    main()
