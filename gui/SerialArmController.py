# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 08:34:29 2020

@author: shill
"""

from serial.tools import list_ports
import serial
from threading import Thread
import time

ARDUINO_VID  = 0x2341
UNO_PID      = 0x0043
LEONARDO_PID = 0x8036

class Command():
    PITCH = 0
    YAW = 1
    ROLL = 2
    CLOSE = 3
    OPEN = 4
    PORTRAIT = 5
    LANDSCAPE = 6
    NOD = 7
    SHAKE = 8
    TILT = 9
    SHUTDOWN = 0x10


class Position:
    def __init__(self, pitch=0, yaw=0, roll=0):
        self.pitch = pitch
        self.yaw = yaw
        self.roll = roll
        
    def __str__(self):
        return "P: {}, Y: {}, R: {}".format(self.pitch, self.yaw, self.roll)

'''
class ConnectionChecker(Thread):
    def __init__(self, _dev, _comport, _notifications, **kwargs):
        super().__init__(**kwargs)
        self.serial_arm_controller = _dev
        self.comport = _comport
        self.notifications = _notifications

    def run(self):
        self.is_connected = True
        while self.is_connected:
            devs = list_ports.comports()
            if self.comport not in devs:
                self.notifications.append_line("WARNING: DEVICE DISCONNECTED")
                self.serial_arm_controller.close()
                return
            time.sleep(1)
'''
        
        
class SerialArmController:
    def __init__(self, _status_bar, _notifications):
        self.status_bar = _status_bar
        self.notifications = _notifications
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
            # self.connection_checker = ConnectionChecker(self, comport, self.notifications)
            # self.connection_checker.setDaemon(True)
            # self.connection_checker.start()
        
    def close(self):
        if self.is_connected:
            self._device.close()
            self.status_bar.set_status("DISCONNECTED")
            self.is_connected = False
            # self.connection_checker.join()
        
    def send(self, data):
        if self.is_connected:
            print("Sending: \"{}\"".format(data))
            self._device.write(data)
        
    def recv(self):
        if self.is_connected:
            data = self._device.read(3)
            print("Received: \"{}\"".format(data))
            return data

    def update_position(self):
        pos = self.recv()
        if pos:
            self.position.pitch = int(pos[0])
            self.position.yaw = int(pos[1])
            self.position.roll = int(pos[2])

    def set_pitch(self, val):
        # val is one byte
        if self.is_connected:
            self.send(bytes((Command.PITCH, val)))
            
    def set_yaw(self, val):
        # val is 1 byte
        if self.is_connected:
            self.send(bytes((Command.YAW, val + 90)))
            
    def set_roll(self, val):
        # val is one byte
        if self.is_connected:
            self.send(bytes((Command.ROLL, val)))
            
    def close_arm(self):
        if self.position.pitch == 0:
            self.notifications.append_line("WARNING: ARM ALREADY CLOSED")
        else:
            self.send(bytes((Command.CLOSE, 0)))
        
    def open_arm(self):
        if self.position.pitch == 90:
            self.notifications.append_line("WARNING: ARM ALREADY OPEN")
        else:
            self.send(bytes((Command.OPEN, 0)))
        
    def portrait(self):
        if self.is_connected:
            if self.position.roll == 0:
                self.notifications.append_line("WARNING: ALREADY IN PORTRAIT")
            else:
                self.send(bytes((Command.PORTRAIT, 0)))
                
    def landscape(self):
        if self.is_connected:
            if self.position.roll == 90:
                self.notifications.append_line("WARNING: ALREADY IN LANDSCAPE")
            else:
                self.send(bytes((Command.LANDSCAPE, 0)))
                
    def tilt(self):
        if self.is_connected:
            self.send(bytes((Command.TILT, 0)))
            
    def nod(self):
        if self.is_connected:
            self.send(bytes((Command.NOD, 0)))
            
    def shake(self):
        if self.is_connected:
            self.send(bytes((Command.SHAKE, 0)))

    def _shutdown(self):
        if self.is_connected:
            self.send(bytes((Command.SHUTDOWN, 0)))
            self.close()
        