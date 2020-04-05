# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 17:10:35 2020

@author: Ben Shiller
"""

import tkinter as tk
import tkinter.ttk as ttk


class ControlButtons(tk.Frame):
    def __init__(self, master, arm_controller, **kwargs):
        super().__init__(master, **kwargs)
        self.serial_arm_controller = arm_controller
        self.open_close_status = "CLOSED"
        self.orientation = "PORTRAIT"
        self.create_buttons()
        
    def create_buttons(self):
        self.top_frame = tk.Frame(self)
        self.top_frame.pack(fill="x")
        
        '''
        # Start/Shutdown button
        self.start_shutdown_text = tk.StringVar()
        self.start_shutdown_text.set("Start")
        self.start_shutdown_btn = ttk.Button(self.top_frame, 
            textvariable=self.start_shutdown_text, command=self.hello)
        self.start_shutdown_btn.pack(side="left")
        #self.start_shutdown_btn.grid(row=0, column=0)
        '''
        
        # Open/Close Arm button
        self.open_close_text = tk.StringVar()
        self.open_close_text.set("Open Arm")
        self.open_close_arm_btn = ttk.Button(self.top_frame,
            textvariable=self.open_close_text, command=self.open_close_arm)
        self.open_close_arm_btn.pack(side="left")
        #self.open_close_arm_btn.grid(row=0, column=1)
        
        '''
        # Portrait/Landscape button
        self.portrait_landscape_text = tk.StringVar()
        self.portrait_landscape_text.set("Change to Landscape")
        self.portrait_landscape_btn = ttk.Button(self.top_frame,
            textvariable=self.portrait_landscape_text, command=self.change_orientation)
        self.portrait_landscape_btn.pack(side="left")
        #self.portrait_landscape_btn.grid(row=0, column=2)
        '''
        
        # Portrait button
        self.portrait_btn = ttk.Button(self.top_frame,
            text="Portrait", command=self.portrait)
        self.portrait_btn.pack(side="left")
        
        self.landscape_btn= ttk.Button(self.top_frame,
            text="Landscape", command=self.landscape)
        self.landscape_btn.pack(side="left")
        
        # Head Tilt button
        self.head_tilt_btn = ttk.Button(self.top_frame,
            text="Tilt Head", command=self.tilt)
        self.head_tilt_btn.pack(side="left")
        #self.head_tilt_btn.grid(row=0, column=3)
        
        self.bottom_frame = tk.Frame(self)
        self.bottom_frame.pack(fill="x")
        
        # Nod Head button
        self.nod_head_btn = ttk.Button(self.bottom_frame,
            text="Nod Head", command=self.nod)
        self.nod_head_btn.pack(side="left")
        #self.nod_head_btn.grid(row=1, column=0)
        
        # Shake Head button
        self.shake_head_btn = ttk.Button(self.bottom_frame,
            text="Shake Head", command=self.shake)
        self.shake_head_btn.pack(side="left")
        #self.shake_head_btn.grid(row=1, column=1)
        
        '''
        # Emergency Shutdown button
        self.emergency_shutdown_btn = ttk.Button(self.bottom_frame,
            text="Emergency Shutdown", command=self.hello)
        self.emergency_shutdown_btn.pack(side="left")
        #self.emergency_shutdown_btn.grid(row=1, column=2)
        '''
        
        
    def open_close_arm(self):
        if self.serial_arm_controller.is_connected:
            if self.open_close_status == "CLOSED":
                print("Opening arm...")
                self.serial_arm_controller.open_arm()
                self.open_close_text.set("Close Arm")
                self.open_close_status = "OPEN"
            else:
                print("Closing arm...")
                self.serial_arm_controller.close_arm()
                self.open_close_text.set("Open Arm")
                self.open_close_status = "CLOSED"
                
    '''
    def change_orientation(self):
        if self.serial_arm_controller.is_connected:
            if self.orientation == "PORTRAIT":
                print("Changing to landscape...")
                self.serial_arm_controller.send("LANDSCAPE")
                self.portrait_landscape_text.set("Change to Portrait")
                self.orientation = "LANDSCAPE"
            else:
                print("Changing to portrait...")
                self.serial_arm_controller.send("PORTRAIT")
                self.portrait_landscape_text.set("Change to Landscape")
                self.orientation = "PORTRAIT"
    '''
                
    def portrait(self):
        if self.serial_arm_controller.is_connected:
            print("Changing to portrait...")
            self.serial_arm_controller.portrait()
            self.orientation = "PORTRAIT"
                
    def landscape(self):
        if self.serial_arm_controller.is_connected:
            print("Changing to landscape...")
            self.serial_arm_controller.landscape()
            self.orientation = "LANDSCAPE"
                
    def tilt(self):
        if self.serial_arm_controller.is_connected:
            print("Tilting head...")
            self.serial_arm_controller.tilt()
            
    def nod(self):
        if self.serial_arm_controller.is_connected:
            print("Nodding head...")
            self.serial_arm_controller.nod()
            
    def shake(self):
        if self.serial_arm_controller.is_connected:
            print("Shaking head...")
            self.serial_arm_controller.shake()
        
    def hello(self):
        print("Hello from ControlButtons")
        self.master.notifications_frame.append_line("Hello from ControlButtons")

