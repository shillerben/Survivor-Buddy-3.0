# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 08:08:16 2020

@author: shill
"""

import tkinter as tk
import tkinter.ttk as ttk

class LabelScaleSpinbox(tk.Frame):
    def __init__(self, master, text="", from_=0, to=10, **kwargs):
        super().__init__(master, **kwargs)
        
        if text:
            self.label = ttk.Label(self, text=text)
            self.label.pack(side="left")
        
        self.from_label = ttk.Label(self, text=str(from_))
        self.from_label.pack(side="left")
        
        self.slider = ttk.Scale(self, from_=from_, to=to, 
            orient="horizontal", length=200)
        self.slider.pack(side="left")
        
        self.to_label = ttk.Label(self, text=str(to))
        self.to_label.pack(side="left")
        
        self.spinbox = ttk.Spinbox(self, from_=from_, to=to, width=4)
        self.spinbox.pack(side="left")
        
        

class PositionFrame(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.render_frame = tk.Frame(self)
        self.render_frame.pack(side="left")
        self.create_render(self.render_frame)
        
        self.control_frame = tk.Frame(self)
        self.control_frame.pack(side="left")
        self.create_controls(self.control_frame)
        
    def create_render(self, master):
        self.render_canvas = tk.Canvas(master, width=200, height=200)
        self.render_canvas.config(bg="red")
        self.render_canvas.pack()
        #master.grid(row=0, column=0, rowspan=3, columnspan=2)
        #self.render_canvas = tk.Canvas(master)
        #self.render_canvas.grid()
        
    def create_controls(self, master):
        self.pitch_control = LabelScaleSpinbox(master, text="Pitch: ", from_=0, to=90)
        self.pitch_control.pack()
        
        self.yaw_control = LabelScaleSpinbox(master, text="Yaw: ", from_=-180, to=180)
        self.yaw_control.pack()
        
        self.roll_control = LabelScaleSpinbox(master, text="Roll: ", from_=-90, to=90)
        self.roll_control.pack()
        '''
        self.pitch_frame = tk.Frame(master)
        self.pitch_frame.pack()
        self.pitch_label = ttk.Label(self.pitch_frame, text="Pitch: ")
        self.pitch_label.pack(side="left")
        self.pitch_slider = ttk.Scale(self.pitch_frame, from_=0, to=90, 
            orient="horizontal", length=400)
        self.pitch_slider.pack(side="left")
        self.pitch_spinbox = ttk.Spinbox(self.pitch_frame, 
            from_=0, to=90)
        self.pitch_spinbox.pack(side="left")
        
        self.yaw_frame = tk.Frame(master)
        self.yaw_frame.pack()
        self.yaw_label = ttk.Label(self.yaw_frame, text="Yaw:  ")
        self.yaw_label.pack(side="left")
        self.yaw_slider = ttk.Scale(self.yaw_frame, from_=0, to=90, 
            orient="horizontal", length=400)
        self.yaw_slider.pack(side="left")
        self.yaw_spinbox = ttk.Spinbox(self.yaw_frame, 
            from_=0, to=90)
        self.yaw_spinbox.pack(side="left")
        
        self.roll_frame = tk.Frame(master)
        self.roll_frame.pack()
        self.roll_label = ttk.Label(self.roll_frame, text="Roll:   ")
        self.roll_label.pack(side="left")
        self.roll_slider = ttk.Scale(self.roll_frame, from_=0, to=90, 
            orient="horizontal", length=400)
        self.roll_slider.pack(side="left")
        self.roll_spinbox = ttk.Spinbox(self.roll_frame, 
            from_=0, to=90)
        self.roll_spinbox.pack(side="left")
        '''
        
