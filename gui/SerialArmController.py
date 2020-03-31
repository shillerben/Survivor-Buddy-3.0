# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 08:34:29 2020

@author: shill
"""

from serial.tools import list_ports
import serial

ARDUINO_VID  = 0x2341
UNO_PID      = 0x0001
LEONARDO_PID = 0x8036


class Position:
    def __init__(self, pitch=0, yaw=0, roll=0):
        self.pitch = pitch
        self.yaw = yaw
        self.roll = roll
        
        
    def __str__(self):
        return "P: {}, Y: {}, R: {}".format(self.pitch, self.yaw, self.roll)
        
        
class SerialArmController:
    def __init__(self, _status_bar):
        self.status_bar = _status_bar
        self._com_port = ""
        self._device = None
        self.devs = []
        self.position = Position()
        self.is_connected = False
     
        
    def update_devs(self):
        devs = list_ports.comports()
        """
        devs is an array of tuples of the form (com port, name)
        """
        self.devs = []
        for dev in devs:
            if dev.vid == ARDUINO_VID and dev.pid == LEONARDO_PID:
                self.devs.append((dev.device, "Leonardo"))
            elif dev.vid == ARDUINO_VID and dev.pid == UNO_PID:
                self.devs.append((dev.device, "Uno"))
           
            
    def connect(self, comport):
        if not self.is_connected:
            self._device = serial.Serial(comport, timeout=1)
            self.status_bar.set_status("CONNECTED")
            self.is_connected = True
        
        
    def close(self):
        if self.is_connected:
            self._device.close()
            self.status_bar.set_status("DISCONNECTED")
            self.is_connected = False
        
        
    def send(self, data):
        if self.is_connected:
            print("Sending: \"{}\"".format(data))
            self._device.write(data.encode())
            self.recv()
        
        
    def recv(self):
        if self.is_connected:
            data = self._device.read(256)
            print("Received: \"{}\"".format(data))
            return self._device.read(256)
    
    
    def get_position(self):
        if self.is_connected:
            print("Called get_position()...")
            self.send("POS")
            response = self.recv()
            print("Received: {}".format(response))
        
        
    def set_position(self, position):
        if self.is_connected:
            print("Called set_position({})...".format(str(position)))
            data = str(position)
            self.send(data)
        