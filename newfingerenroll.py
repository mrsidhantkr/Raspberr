#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Fingerprint Enrollment Script for AI Contactless Door System
"""

import time
from pyfingerprint.pyfingerprint import PyFingerprint
from lcd_module import display_message  # Import the LCD module

## Enrolls new finger ##
def enroll_fingerprint():
    try:
        # Initialize the fingerprint sensor
        f = PyFingerprint('/dev/ttyS0', 57600, 0xFFFFFFFF, 0x00000000)

        if not f.verifyPassword():
            raise ValueError('The given fingerprint sensor password is wrong!')

    except Exception as e:
        print('The fingerprint sensor could not be initialized!')
        print('Exception message: ' + str(e))
        display_message("Sensor Error!", duration=3)
        return

    ## Display sensor information
    print(f'Currently used templates: {f.getTemplateCount()}/{f.getStorageCapacity()}')

    ## Try to enroll a new finger
    try:
        print('Waiting for finger...')
        display_message("Place Finger...", duration=5)

        # Wait until a finger is detected
        while not f.readImage():
            pass

        # Convert the read image to characteristics and store it in charbuffer 1
        f.convertImage(0x01)

        # Check if the finger is already enrolled
        result = f.searchTemplate()
        positionNumber = result[0]

        if positionNumber >= 0:
            print(f'Template already exists at position #{positionNumber}')
            display_message("Finger Exists!", duration=3)
            return

        print('Remove finger...')
        display_message("Remove Finger", duration=3)
        time.sleep(2)

        print('Waiting for same finger again...')
        display_message("Place Finger Again", duration=5)

        # Wait until the same finger is detected
        while not f.readImage():
            pass

        # Convert the read image to characteristics and store it in charbuffer 2
        f.convertImage(0x02)

        # Compare the charbuffers
        if f.compareCharacteristics() == 0:
            raise Exception('Fingers do not match')

        # Create a template
        f.createTemplate()

        # Save the template at a new position number
        positionNumber = f.storeTemplate()
        print('Finger enrolled successfully!')
        print(f'New template position #{positionNumber}')
        display_message("Enroll Success!", duration=3)

    except Exception as e:
        print('Operation failed!')
        print(f'Exception message: {e}')
        display_message("Enroll Failed!", duration=3)

## Main Program ##
if __name__ == "__main__":
    enroll_fingerprint()
