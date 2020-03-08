# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 14:17:02 2020

@author: shill
"""

import tkinter as tk
import tkinter.ttk as ttk

class StatusBar(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.status_frame = tk.Frame(self)
        self.status_frame.pack(side="left")
        #self.status_frame.grid(row=0, column=0, sticky=tk.W)
        
        self.status_label = ttk.Label(self.status_frame, text="Status:")
        self.status_label.pack(side="left")
        #self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        self.status_text = tk.StringVar()
        self.status_text.set("OFF")
        self.status_text_label = ttk.Label(
            self.status_frame, textvariable=self.status_text)
        self.status_text_label.pack(side="left")
        #self.status_text_label.grid(row=0, column=1, sticky=tk.W)
        
        
        self.orientation_frame = tk.Frame(self)
        self.orientation_frame.pack(side="right")
        #self.orientation_frame.grid(row=0, column=1, sticky=tk.E)
        
        self.orientation_label = ttk.Label(self.orientation_frame, text="Orientation:")
        self.orientation_label.pack(side="left")
        #self.orientation_label.grid(row=0, column=0)
        
        self.orientation_text = tk.StringVar()
        self.orientation_text.set("PORTRAIT")
        self.orientation_text_label = ttk.Label(
            self.orientation_frame, textvariable=self.orientation_text)
        self.orientation_text_label.pack(side="left")
        #self.orientation_text_label.grid(row=0, column=1)
