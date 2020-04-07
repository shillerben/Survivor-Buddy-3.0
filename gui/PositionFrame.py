# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 08:08:16 2020

@author: Ben Shiller, Philip Rettenmaier
"""

import tkinter as tk
import tkinter.ttk as ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

class LabelScaleSpinbox(tk.Frame):
    def __init__(self, master, text="", from_=0, to=10, axis=0, dev=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.min = from_
        self.max = to
        self.axis = axis
        self.serial_arm_controller = dev
        
        if text:
            self.label = ttk.Label(self, text=text)
            self.label.pack(side="left")
        
        self.from_label = ttk.Label(self, text=str(from_))
        self.from_label.pack(side="left")
        
        self.slider = ttk.Scale(self, from_=from_, to=to, orient="horizontal", length=200)
        self.slider.bind("<ButtonRelease-1>", self.sliderUpdate)
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
        #self.send_command()
        
    def sliderUpdate(self, val):
        print('Slider Update')
        newVal = int(self.slider.get())
        self.spinbox.set(newVal)    #Update spinbox value
        self.current_value = newVal
        self.send_command()
        
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
        except:
            print("Error: Input must be a number")
            return
        self.slider.set(val)
        self.current_value = val
        self.send_command()
        #self.serial_arm_controller.recv()
    
    def send_command(self):
        if self.axis == 0:  #Pitch
            self.serial_arm_controller.set_pitch(self.current_value) if self.serial_arm_controller.is_connected else print('Device Disconnected')
            PositionFrame.pitch = self.current_value
        elif self.axis == 1:    #Yaw
            self.serial_arm_controller.set_yaw(self.current_value) if self.serial_arm_controller.is_connected else print('Device Disconnected')
            PositionFrame.yaw = self.current_value
        elif self.axis == 2:    #Roll
            self.serial_arm_controller.set_roll(self.current_value) if self.serial_arm_controller.is_connected else print('Device Disconnected')   
            PositionFrame.roll = self.current_value

class PositionFrame(tk.Frame):
    def __init__(self, master, arm_controller, **kwargs):
        super().__init__(master, **kwargs)
        
        self.serial_arm_controller = arm_controller
        
        self.render_frame = tk.Frame(self)
        self.render_frame.pack(side="left")
        self.create_render(self.render_frame)
        
        self.control_frame = tk.Frame(self)
        self.control_frame.pack(side="left")
        self.create_controls(self.control_frame)
        self.yaw = 100
        self.pitch = 100
        self.roll = 100
        
    def create_render(self, master):      
        # Disable plot toolbar
        mpl.rcParams['toolbar'] = 'None'

        # Set up 3d plot, define size
        fig = plt.figure(figsize=(3,3))
        ax = fig.gca(projection='3d')

        # Remove unneccesary information from plot
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_zticklabels([])
        ax.legend().remove()

        # Draw x, y and z axes to make plot easier to read, set plot size
        ax.quiver(-2, 0, 0, 4, 0, 0, length=1.0, arrow_length_ratio=0, color = '#cf685d')
        ax.quiver(0, -2, 0, 0, 4, 0, length=1.0, arrow_length_ratio=0, color = '#5d5fcf')
        ax.quiver(0, 0, -2, 0, 0, 4, length=1.0, arrow_length_ratio=0, color = '#6ad15e')
        ax.set_xlim(left=-2, right=2, emit=True, auto=False)
        ax.set_ylim(bottom=-2, top=2, emit=True, auto=False)
        ax.set_zlim(bottom=-2, top=2, emit=True, auto=False)

        ax.quiver(0, 0, 0, 1, 1, 0, length=1.0)

        self.render_canvas = FigureCanvasTkAgg(fig, master)
        self.render_canvas.get_tk_widget().grid(row=1,column=1,rowspan = 4)
        
    def create_controls(self, master):
        self.pitch_control = LabelScaleSpinbox(
            master, text="Pitch: ", from_=0, to=90, axis=0, dev=self.serial_arm_controller)
        self.pitch_control.pack()
        
        self.yaw_control = LabelScaleSpinbox(
            master, text="Yaw: ", from_=-180, to=180, axis=1, dev=self.serial_arm_controller)
        self.yaw_control.pack()
        
        self.roll_control = LabelScaleSpinbox(
            master, text="Roll: ", from_=-90, to=90, axis=2, dev=self.serial_arm_controller)
        self.roll_control.pack()
        