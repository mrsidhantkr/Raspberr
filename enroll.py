import time
import serial
import adafruit_fingerprint

# Initialize the serial connection
uart = serial.Serial("/dev/serial0", baudrate=57600, timeout=1)

# Create a fingerprint sensor instance
fingerprint = adafruit_fingerprint.Adafruit_Fingerprint(uart)

def get_fingerprint_image():
    print("Place your finger on the sensor...")
    while fingerprint.get_image() != adafruit_fingerprint.OK:
        pass
    print("Image taken")

    if fingerprint.image_2_tz(1) != adafruit_fingerprint.OK:
        print("Failed to process the image. Try again.")
        return False

    return True

def enroll_fingerprint(slot):
    print(f"Enrolling fingerprint in slot {slot}.")

    print("Step 1: Capture the first fingerprint image.")
    if not get_fingerprint_image():
        return False

    print("Remove your finger.")
    time.sleep(2)
    while fingerprint.get_image() == adafruit_fingerprint.OK:
        pass

    print("Step 2: Capture the second fingerprint image.")
    if not get_fingerprint_image():
        return False

    print("Creating a fingerprint model...")
    if fingerprint.create_model() != adafruit_fingerprint.OK:
        print("Failed to create a fingerprint model.")
        return False

    print(f"Storing the fingerprint model in slot {slot}...")
    if fingerprint.store_model(slot) != adafruit_fingerprint.OK:
        print("Failed to store the fingerprint model.")
        return False

    print("Fingerprint enrolled successfully!")
    return True

if __name__ == "__main__":
    try:
        # Select a slot number for enrollment (1-127)
        slot_number = int(input("Enter a slot number to save the fingerprint (1-127): "))
        if not (1 <= slot_number <= 127):
            print("Invalid slot number. Please enter a number between 1 and 127.")
        else:
            if enroll_fingerprint(slot_number):
                print("Enrollment complete.")
            else:
                print("Enrollment failed. Please try again.")
    except Exception as e:
        print(f"An error occurred: {e}")
