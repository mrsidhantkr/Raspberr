import serial
import adafruit_fingerprint

# Define the UART port and baud rate
UART_PORT = "/dev/ttyS0"  # Replace with "/dev/ttyAMA0" if needed
BAUD_RATE = 57600

def check_sensor_connection():
    try:
        # Initialize UART connection
        uart = serial.Serial(UART_PORT, baudrate=BAUD_RATE, timeout=1)
        
        # Initialize fingerprint sensor
        fingerprint = adafruit_fingerprint.Adafruit_Fingerprint(uart)
        
        # Verify the sensor password (default password is 0xFFFFFFFF)
        if fingerprint.verify_password() == adafruit_fingerprint.OK:
            print("Fingerprint sensor is connected and responding!")
        else:
            print("Failed to communicate with the fingerprint sensor. Check connections and settings.")
    except serial.SerialException as e:
        print(f"Serial port error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    print("Checking fingerprint sensor connection...")
    check_sensor_connection()
