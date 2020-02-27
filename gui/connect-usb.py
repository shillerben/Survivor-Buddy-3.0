# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 21:15:44 2020

@author: Ben Shiller
"""

from serial.tools import list_ports
import serial
import sys

ARDUINO_VID  = 0x2341
UNO_PID      = 0x0001
LEONARDO_PID = 0x8036

devs = list_ports.comports()

arduino_com_port = ""

for dev in devs:
    if dev.vid == ARDUINO_VID and dev.pid == LEONARDO_PID:
        print("Found Arduino Leonardo.")
        arduino_com_port = dev.device
    elif dev.vid == ARDUINO_VID and dev.pid == UNO_PID:
        print("Found Arduino Uno.")
        arduino_com_port = dev.device

if arduino_com_port == "":
    print("No arduino found.")
    sys.exit()
    
serial_port = serial.Serial(arduino_com_port, timeout=1)
print("Connected to Arduino on {}".format(dev.device))
send_data = ""
while True:
    send_data = input("Enter a message: ")
    if send_data == "q":
        break
    if send_data:
        print("Sending {}...".format(send_data))
        serial_port.write(send_data.encode())
        response = serial_port.read(256)
        print("Received: {}".format(response))
serial_port.close()

'''
for dev in devs:
    print("device: {}".format(dev.device))
    print("name: {}".format(dev.name))
    print("description: {}".format(dev.description))
    print("hwid: {}".format(dev.hwid))
    print("vid: 0x{:x}".format(int(dev.vid)))
    print("pid: 0x{:x}".format(int(dev.pid)))
    print("serial_number: {}".format(dev.serial_number))
    print("location: {}".format(dev.location))
    print("manufacturer: {}".format(dev.manufacturer))
    print("product: {}".format(dev.product))
    print("interface: {}".format(dev.interface))
    '''
    