# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 13:27:15 2020

@author: shill
"""

import tkinter as tk
import tkinter.ttk as ttk

class NotificationFrame(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        
        self.label = ttk.Label(self, text="Notifications")
        self.label.grid()
        
        self.scrollbar = ttk.Scrollbar(self)
        self.scrollbar.grid()
        
        self.text = tk.Text(self.scrollbar)
        self.text.config(state=tk.DISABLED)
        self.text.grid()
        
    def append_line(self, line):
        self.text.config(state=tk.NORMAL)
        self.text.insert(tk.END, line + "\n")
        self.text.config(state=tk.DISABLED)
        
        