# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 14:17:02 2020

@author: shill
"""

import tkinter as tk
import tkinter.ttk as ttk

class StatusBar(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        
        self.status_label = ttk.Label(self, text="Status:")
        self.status_label.grid(row=0, column=0)
        
        self.status_text = tk.StringVar()
        self.status_text.set("OFF")
        self.status_text_label = ttk.Label(
            self, textvariable=self.status_text)
        self.status_text_label.grid(row=0, column=1)
        
        self.orientation_label = ttk.Label(self, text="Orientation:")
        self.orientation_label.grid(row=0, column=2)
        
        self.orientation_text = tk.StringVar()
        self.orientation_text.set("PORTRAIT")
        self.orientation_text_label = ttk.Label(
            self, textvariable=self.orientation_text)
        self.orientation_text_label.grid(row=0, column=3)
