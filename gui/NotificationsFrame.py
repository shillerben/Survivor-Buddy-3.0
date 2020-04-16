# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 13:27:15 2020

@author: shill
"""

import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime

class NotificationFrame(tk.Frame):
    def __init__(self, master, _logFile, **kwargs):
        super().__init__(master, **kwargs)
        
        self.logFile = _logFile
        self.label = ttk.Label(self, text="Notifications")
        self.label.pack()
        #self.label.grid(row=0, rowspan=1, sticky="w")
        
        self.scrollbar = ttk.Scrollbar(self)
        self.scrollbar.pack(fill="x", expand=1)
        #self.scrollbar.grid(row=1, rowspan=3, sticky="w")
        
        self.text = tk.Text(self.scrollbar, height=4)
        self.text.config(state=tk.DISABLED)
        self.text.pack()
        #self.text.grid()
        
    def append_line(self, line):
        self.text.config(state=tk.NORMAL)
        self.text.insert(tk.END, line + "\n")
        now = datetime.now()
        timestamp = now.strftime("%H:%M:%S")
        self.logFile.write(timestamp + " - " + line + "\n") #Print notification to external log file
        self.text.see(tk.END)   #Scrolls down to show latest notification automatically
        self.text.config(state=tk.DISABLED)
        
        
        