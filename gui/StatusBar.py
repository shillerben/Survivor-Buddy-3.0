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
        
        # STATUS #
        self.status_frame = tk.Frame(self)
        self.status_frame.pack(side="left")
        
        self.status_label = ttk.Label(self.status_frame, text="Status:")
        self.status_label.pack(side="left")
        
        self.status_text = tk.StringVar()
        self.status_text.set("DISCONNECTED")
        self.status_text_label = ttk.Label(
            self.status_frame, textvariable=self.status_text)
        self.status_text_label.pack(side="left")

        ''' Might get rid of this because it doesn't seem useful anymore
        # ORIENTATION #
        self.orientation_frame = tk.Frame(self)
        self.orientation_frame.pack(side="right")
        
        self.orientation_label = ttk.Label(self.orientation_frame, text="Orientation:")
        self.orientation_label.pack(side="left")
        
        self.orientation_text = tk.StringVar()
        self.orientation_text.set("N/A")
        self.orientation_text_label = ttk.Label(
            self.orientation_frame, textvariable=self.orientation_text)
        self.orientation_text_label.pack(side="left")
        '''


    def set_status(self, status):
        #print("set_status({})".format(status))
        self.status_text.set(status)
        
        
    def set_orientation(self, orientation):
        self.orientation_text.set(orientation)
        #print("set_orientation({})".format(orientation))
