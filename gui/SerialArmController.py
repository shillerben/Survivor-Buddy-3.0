# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 08:34:29 2020

@author: shill
"""

from serial.tools import list_ports
import serial
import sys

ARDUINO_VID  = 0x2341
UNO_PID      = 0x0001
LEONARDO_PID = 0x8036


class Value:
    def __init__(self, val):
        self.value = val
        

class Position:
    def __init__(self, pitch=0, yaw=0, roll=0):
        self.pitch_ref = Value(pitch)
        self.yaw_ref = Value(yaw)
        self.roll_ref = Value(roll)
        
        
    def get_pitch(self):
        return self.pitch_ref.value

    def set_pitch(self, val):
        self.pitch_ref.value = val
        
    
    def get_yaw(self):
        return self.yaw_ref.value
    
    def set_yaw(self, val):
        self.yaw_ref.value = val
    
    
    def get_roll(self):
        return self.roll_ref.value
    
    def set_roll(self, val):
        self.roll_ref.value = val
        
        
    def __str__(self):
        return "P: {}, Y: {}, R: {}".format(
            self.get_pitch(), self.get_yaw(), self.get_roll())


class SerialArmController:
    def __init__(self):
        self._com_port = ""
        self._device = None
        self.devs = []
     
        
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
        self._device = serial.Serial(comport, timeout=1)
        
        
    def close(self):
        self._device.close()
        
        
    def send(self, data):
        self._device.write(data.encode())
        
        
    def recv(self):
        return self._device.read(256)
    
    
    def get_position(self):
        print("Called get_position()...")
        self.send("POS")
        response = self.recv()
        print("Received: {}".format(response))
        
        
    def set_position(self, position):
        print("Called set_position({})...".format(str(position)))
        data = str(position)
        self.send(data)
        