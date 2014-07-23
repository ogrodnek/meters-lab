#!/usr/bin/env python

import time
from pyfirmata import Arduino

arduino = Arduino('/dev/tty.usbmodem1421')
meter1 = arduino.get_pin('d:5:p')
meter2 = arduino.get_pin('d:6:p')

def write(val):
    meter1.write(val * 0.01)
    meter2.write(val * 0.01)
    time.sleep(0.05)

while True:
    for x in range(0, 101):
        write(x)
        
    for x in range(100, -1, -1):
        write(x)
