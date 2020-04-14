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
from threading import Thread
import time
import queue

class PositionUpdater(Thread):
    def __init__(self, dev, _pitch_control, _yaw_control, _roll_control, _render_queue, **kwargs):
        super().__init__(**kwargs)
        self.serial_arm_controller = dev
        self.pitch_control = _pitch_control
        self.yaw_control = _yaw_control
        self.roll_control = _roll_control
        self.render_queue = _render_queue

    def run(self):
        yaw = 0
        pitch = 0
        roll = 0
        while True:
            if self.serial_arm_controller.is_connected: #If else to allow testing of GUI without connected arm
                self.serial_arm_controller.update_position()
                self.pitch_control.slider.set(pitch)
                self.pitch_control.spinbox.set(pitch)
                self.yaw_control.slider.set(yaw)
                self.yaw_control.spinbox.set(yaw)
                self.roll_control.slider.set(roll)
                self.roll_control.spinbox.set(roll)

                pitch = self.serial_arm_controller.position.pitch
                yaw = self.serial_arm_controller.position.yaw
                roll = self.serial_arm_controller.position.roll
            else:
                pitch = self.pitch_control.spinbox.get()
                yaw = self.yaw_control.spinbox.get()
                roll = self.roll_control.spinbox.get()
            if (self.render_queue.empty()):   #Only add to queue if queue is empty, otherwise will fill with values, getting out of sync with render and memory leak
                self.render_queue.put(yaw)
            time.sleep(0.1)


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
        
    def sliderUpdate(self, val):
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
    
    def send_command(self):
        if self.serial_arm_controller.is_connected:
            self.serial_arm_controller.set_pitch(self.current_value)
        

class RenderDiagram(tk.Frame): 
    def __init__(self, master, dev=None, **kwargs):
        super().__init__(master, **kwargs)

        self.serial_arm_controller = dev

        # Disable plot toolbar
        mpl.rcParams['toolbar'] = 'None'

        # Set up 3d plot, define size
        self.fig = plt.figure(figsize=(3,3))
        self.ax = self.fig.gca(projection='3d')

        self.draw_axes() #Split into separate function, as axes must be redrawn each frame

        self.render_canvas = FigureCanvasTkAgg(self.fig, master)
        self.render_canvas.get_tk_widget().pack()
    
    def draw_axes(self):
        # Remove unneccesary information from plot
        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])
        self.ax.set_zticklabels([])

        # Draw x, y and z axes to make plot easier to read, set plot size
        self.ax.quiver(-2, 0, 0, 4, 0, 0, length=1.0, arrow_length_ratio=0, color = '#cf685d')
        self.ax.quiver(0, -2, 0, 0, 4, 0, length=1.0, arrow_length_ratio=0, color = '#5d5fcf')
        self.ax.quiver(0, 0, -2, 0, 0, 4, length=1.0, arrow_length_ratio=0, color = '#6ad15e')
        self.ax.set_xlim(left=-2, right=2, emit=True, auto=False)
        self.ax.set_ylim(bottom=-2, top=2, emit=True, auto=False)
        self.ax.set_zlim(bottom=-2, top=2, emit=True, auto=False)

    def update_render(self, master, yaw, pitch, roll):   #will implement if I can figure out how to update plot
        self.ax.clear() #clear old data
        self.draw_axes()    #redraw axes
        self.ax.quiver(0, 0, 0, yaw, 2, 3, length=10.0, arrow_length_ratio=0)
        self.render_canvas.draw()

    def delete_render(self):
        plt.close()

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

        self.render_queue = queue.LifoQueue()

        self.create_updater()
        self.frame_master = self.render_frame    #s.t. master does not have to be passed to process queue
        self.master.after(100, self.process_queue)

        
    def create_render(self, master):    
        self.pos_render = RenderDiagram(
            master, dev=self.serial_arm_controller
        )
        self.pos_render.pack()
        
    def create_controls(self, master):
        self.pitch_control = LabelScaleSpinbox(
            master, text="Pitch: ", from_=0, to=90, axis=0, dev=self.serial_arm_controller)
        self.pitch_control.pack()
        
        self.yaw_control = LabelScaleSpinbox(
            master, text="Yaw: ", from_=-90, to=90, axis=1, dev=self.serial_arm_controller)
        self.yaw_control.pack()
        
        self.roll_control = LabelScaleSpinbox(
            master, text="Roll: ", from_=0, to=90, axis=2, dev=self.serial_arm_controller)
        self.roll_control.pack()

    def create_updater(self):   #Updater for sliders and render
        self.update_thread = PositionUpdater(
            self.serial_arm_controller,
            self.pitch_control,
            self.yaw_control,
            self.roll_control,
            self.render_queue
        )
        self.update_thread.start()

    def process_queue(self):
        if(not self.render_queue.empty()):
            msg = self.render_queue.get(0)
            self.pos_render.update_render(self.frame_master, msg, 0, 0)
        self.master.after(50, self.process_queue)

        