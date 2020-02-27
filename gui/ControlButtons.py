# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 17:10:35 2020

@author: Ben Shiller
"""

import tkinter as tk
import tkinter.ttk as ttk

class ControlButtons(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.create_buttons()
        
    def create_buttons(self):
        # Start/Shutdown button
        self.start_shutdown_text = tk.StringVar()
        self.start_shutdown_text.set("Start")
        self.start_shutdown_btn = ttk.Button(self, 
            textvariable=self.start_shutdown_text, command=self.hello)
        self.start_shutdown_btn.grid(row=0, column=0)
        
        # Open/Close Arm button
        self.open_close_text = tk.StringVar()
        self.open_close_text.set("Open Arm")
        self.open_close_arm_btn = ttk.Button(self,
            textvariable=self.open_close_text, command=self.hello)
        self.open_close_arm_btn.grid(row=0, column=1)
        
        # Portrait/Landscape button
        self.portrait_landscape_text = tk.StringVar()
        self.portrait_landscape_text.set("Change to Landscape")
        self.open_close_arm_btn = ttk.Button(self,
            textvariable=self.portrait_landscape_text, command=self.hello)
        self.open_close_arm_btn.grid(row=0, column=2)
        
        # Head Tilt button
        self.head_tilt_btn = ttk.Button(self,
            text="Tilt Head", command=self.hello)
        self.head_tilt_btn.grid(row=0, column=3)
        
        # Nod Head button
        self.nod_head_btn = ttk.Button(self,
            text="Nod Head", command=self.hello)
        self.nod_head_btn.grid(row=1, column=0)
        
        # Shake Head button
        self.shake_head_btn = ttk.Button(self,
            text="Shake Head", command=self.hello)
        self.shake_head_btn.grid(row=1, column=1)
        
        # Emergency Shutdown button
        self.emergency_shutdown_btn = ttk.Button(self,
            text="Emergency Shutdown", command=self.hello)
        self.emergency_shutdown_btn.grid(row=1, column=2)
        
        
    def hello(self):
        print("Hello from ControlButtons")
        self.master.notifications_frame.append_line("Hello from ControlButtons")

