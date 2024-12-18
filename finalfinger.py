import serial
import time

def test_fingerprint_sensor():
    try:
        # Open a serial connection to the R307 sensor
        ser = serial.Serial(
            port='/dev/serial0',  # Use /dev/serial0 for Raspberry Pi 3B+ UART
            baudrate=57600,
            timeout=1
        )
        
        if ser.isOpen():
            print("Serial port opened successfully!")
        else:
            print("Failed to open serial port.")
            return False

        # Send a "handshake" packet to test the connection
        # R307 command packet: [0xEF, 0x01] + [0xFF, 0xFF, 0xFF, 0xFF] + [0x01] + [0x00, 0x03, 0x01, 0x00, 0x05]
        handshake_packet = b'\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x03\x01\x00\x05'
        ser.write(handshake_packet)
        print("Handshake packet sent. Waiting for response...")

        # Wait for response
        response = ser.read(12)  # Read 12 bytes (expected length of response)
        if response:
            print("Received response from sensor:", response.hex())
            if response[:6] == b'\xEF\x01\xFF\xFF\xFF\xFF':  # Check header
                print("R307 fingerprint sensor is successfully connected!")
                return True
            else:
                print("Invalid response header. Check connections.")
                return False
        else:
            print("No response received. Check sensor and connections.")
            return False

    except Exception as e:
        print(f"Error: {e}")
        return False

    finally:
        if 'ser' in locals() and ser.isOpen():
            ser.close()
            print("Serial port closed.")

if __name__ == "__main__":
    if test_fingerprint_sensor():
        print("Fingerprint sensor test successful!")
    else:
        print("Fingerprint sensor test failed.")
