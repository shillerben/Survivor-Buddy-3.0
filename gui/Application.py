# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 08:21:08 2020

@author: Ben Shiller
"""

import tkinter as tk
import tkinter.ttk as ttk
from ControlButtons import ControlButtons

class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.create_widgets()
        
    def create_widgets(self):
        self.menu_bar = tk.Menu(self)
        self.create_menu(self.menu_bar)
        
        self.control_buttons = ControlButtons(self)
        self.control_buttons.grid()
        
        self.quit_button = ttk.Button(self, text="Quit", command=self.quit)
        self.quit_button.grid()
        
        self.master.config(menu=self.menu_bar)
        
    def create_menu(self, root_menu):
        # File Menu
        self.file_menu = tk.Menu(root_menu, tearoff=0)
        self.file_menu.add_command(label="Preferences", command=self.hello)
        self.file_menu.add_command(label="Quit", command=self.quit)
        root_menu.add_cascade(label="File", menu=self.file_menu)
        
        # Device Menu
        self.device_menu = tk.Menu(root_menu, tearoff=0)
        self.device_menu.add_command(label="COM 4: Uno", command=self.hello)
        root_menu.add_cascade(label="Device", menu=self.device_menu)
        
        # Gesture Menu
        self.gesture_menu = tk.Menu(root_menu, tearoff=0)
        self.gesture_menu.add_command(label="Nod", command=self.hello)
        self.gesture_menu.add_command(label="Shake Head", command=self.hello)
        self.gesture_menu.add_command(label="Tilt Head", command=self.hello)
        root_menu.add_cascade(label="Gesture", menu=self.gesture_menu)
        
        # Help Menu
        self.help_menu = tk.Menu(root_menu, tearoff=0)
        self.help_menu.add_command(label="Getting Started", command=self.hello)
        self.help_menu.add_command(label="Troubleshooting", command=self.hello)
        self.help_menu.add_command(label="Programmer's Reference", command=self.hello)
        self.help_menu.add_command(label="About Survivor Buddy 3.0", command=self.hello)
        root_menu.add_cascade(label="Help", menu=self.help_menu)

    def hello(self):
        print("Hello")
        
        
root = tk.Tk()
root.geometry("800x600")
app = Application(master=root)
app.master.title("Survivor Buddy 3.0")
app.mainloop()