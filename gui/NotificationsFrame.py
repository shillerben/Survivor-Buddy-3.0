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
        
        