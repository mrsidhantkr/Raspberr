import time
import serial
from adafruit_fingerprint import Adafruit_Fingerprint

# Initialize UART communication
uart = serial.Serial("/dev/serial0", baudrate=57600, timeout=1)

# Initialize the fingerprint sensor
finger = Adafruit_Fingerprint(uart)

# Function to check sensor connection
def get_fingerprint_sensor_status():
    if finger.verify_password():
        print("Sensor initialized successfully!")
    else:
        print("Failed to find fingerprint sensor. Check connections!")

# Main program
if __name__ == "__main__":
    get_fingerprint_sensor_status()
