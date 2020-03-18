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
        
        self.min = from_
        self.max = to
        
        if text:
            self.label = ttk.Label(self, text=text)
            self.label.pack(side="left")
        
        self.from_label = ttk.Label(self, text=str(from_))
        self.from_label.pack(side="left")
        
        self.slider = ttk.Scale(self, from_=from_, to=to, 
            orient="horizontal", length=200, command=self.set_spinbox)
        self.slider.pack(side="left")
        
        self.to_label = ttk.Label(self, text=str(to))
        self.to_label.pack(side="left")
        
        spinbox_vcmd = self.register(self.validate_spinbox)
        spinbox_ivcmd = self.register(self.invalid_spinbox)
        self.spinbox = ttk.Spinbox(self, from_=from_, to=to, width=4, 
            command=self.set_slider, validate="focusout", 
            validatecommand=(spinbox_vcmd, "%P"),
            invalidcommand=(spinbox_ivcmd,))
        
        self.current_value = self.slider.get()
        self.spinbox.set(self.current_value)
        self.spinbox.pack(side="left")
        
        
    def set_spinbox(self, event):
        self.current_value = self.slider.get()
        self.spinbox.set(str(round(self.current_value)))
        
        
    def validate_spinbox(self, val):
        try:
            ival = int(val)
            if ival < self.min or ival > self.max:
                self.spinbox.set(str(round(self.current_value)))
                return False
            else:
                # input is good. Set Slider value
                self.slider.set(ival)
                return True
        except:
            self.spinbox.set(str(round(self.current_value)))
            return False
        
        
    def invalid_spinbox(self):
        print("Error: Position input must be a number between {} and {}".format(self.min, self.max))
        
        
    def set_slider(self):
        try:
            val = int(self.spinbox.get())
            print(val)
        except:
            print("Error: Input must be a number")
            return
        self.slider.set(val)
        
        
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
        
        
    def create_controls(self, master):
        self.pitch_control = LabelScaleSpinbox(master, text="Pitch: ", from_=0, to=90)
        self.pitch_control.pack()
        
        self.yaw_control = LabelScaleSpinbox(master, text="Yaw: ", from_=-180, to=180)
        self.yaw_control.pack()
        
        self.roll_control = LabelScaleSpinbox(master, text="Roll: ", from_=-90, to=90)
        self.roll_control.pack()
        