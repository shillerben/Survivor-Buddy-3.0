# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 08:21:08 2020

@author: Ben Shiller
"""

import tkinter as tk
import tkinter.ttk as ttk
from PositionFrame import PositionFrame
from ControlButtons import ControlButtons
from NotificationsFrame import NotificationFrame
from StatusBar import StatusBar
from SerialArmController import SerialArmController
from datetime import datetime   #For log file formatting
import os.path


class Application(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.pack()
        self.taskbar_icon = tk.PhotoImage(file="SBLogo.png")
        self.master.call('wm', 'iconphoto', self.master._w, self.taskbar_icon)
        self.config(padx=16, pady=16)
        # need the status bar to give to the arm controller
        self.status_bar = StatusBar(self)
        self.serial_arm_controller = SerialArmController(self.status_bar)
        
        now = datetime.now()    #Create unique logfile for notifications and errors
        timestamp = now.strftime("%m_%d_%Y_%H_%M_%S")
        file_name = 'LOGFILE_' + timestamp +'.txt'
        # self.logFile = open(file_name, 'w+')
        
        self.logFile = open(os.path.join(os.path.realpath('../gui/logs/'), file_name) , 'w+')   #Save logfile to log folder

        self.create_widgets()
        
        
    def create_widgets(self):
        self.menu_bar = tk.Menu(self)
        self.create_menu(self.menu_bar)
        
        self.position_frame = PositionFrame(self, self.serial_arm_controller)
        self.position_frame.pack(fill="x")
        
        self.notifications_frame = NotificationFrame(self, self.logFile)

        self.control_buttons = ControlButtons(self, self.serial_arm_controller, self.notifications_frame)
        self.control_buttons.pack(fill="x")
        
        self.notifications_frame.pack(fill="x")
        
        self.status_bar.pack(fill="x")
        
        self.master.config(menu=self.menu_bar)

    def close_app(self):    #Had to make new quit function to close file
        self.logFile.close()
        self.quit()

    def create_menu(self, root_menu):
        # File Menu
        self.file_menu = tk.Menu(root_menu, tearoff=0)
        #self.file_menu.add_command(label="Preferences", command=self.hello)
        self.file_menu.add_command(label="Quit", command=self.close_app)
        root_menu.add_cascade(label="File", menu=self.file_menu)
        
        # Device Menu
        self.device_menu = tk.Menu(root_menu, tearoff=0)
        
        self.device_menu.add_command(label="Refresh Devices", command=self.refresh_devices)
        self.device_menu.add_separator()
        
        root_menu.add_cascade(label="Device", menu=self.device_menu)
        
        '''
        # Gesture Menu
        self.gesture_menu = tk.Menu(root_menu, tearoff=0)
        self.gesture_menu.add_command(label="Nod", command=self.hello)
        self.gesture_menu.add_command(label="Shake Head", command=self.hello)
        self.gesture_menu.add_command(label="Tilt Head", command=self.hello)
        root_menu.add_cascade(label="Gesture", menu=self.gesture_menu)
        '''
        
        # Help Menu
        self.help_menu = tk.Menu(root_menu, tearoff=0)
        self.help_menu.add_command(label="Getting Started", command=self.hello)
        self.help_menu.add_command(label="Troubleshooting", command=self.hello)
        self.help_menu.add_command(label="Programmer's Reference", command=self.hello)
        self.help_menu.add_command(label="About Survivor Buddy 3.0", command=self.hello)
        root_menu.add_cascade(label="Help", menu=self.help_menu)


    def refresh_devices(self):
        self.device_menu.delete(2, 100)
        self.serial_arm_controller.update_devs()
        if not self.serial_arm_controller.devs:
            self.device_menu.add_command(label="No devices", state=tk.DISABLED)
        else:
            for dev in self.serial_arm_controller.devs:
                self.device_menu.add_command(
                    label="{}: {}".format(dev[0], dev[1]),
                    command=lambda: self.connect(dev)
                )        
            
    def connect(self, dev):
        self.serial_arm_controller.connect(dev[0])
        self.device_menu.add_command(
            label="Close Connection",
            command=self.close
        )
    
    def close(self):
        self.device_menu.delete(2 + len(self.serial_arm_controller.devs))
        self.serial_arm_controller.close()
        
    def hello(self):
        print("Hello from Menu")
        self.notifications_frame.append_line("Hello from Menu")
        
        

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    app = Application(master=root)
    app.master.title("Survivor Buddy 3.0")
    app.mainloop()