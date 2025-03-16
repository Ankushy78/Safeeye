import random
import time

VIBRATION_THRESHOLD = 70  

def simulate_vibration():
    return random.randint(0, 100)

def detect_intruder(vibration_value):
    return vibration_value > VIBRATION_THRESHOLD

def vibration_monitor():
    print("Vibration monitoring started...")

    while True:
        vibration_value = simulate_vibration()
        print(f"Vibration Value: {vibration_value}")

        if detect_intruder(vibration_value):
            print("Intruder Detected! Vibration exceeds threshold!")

        time.sleep(1)

if __name__ == "__main__":
    vibration_monitor()
