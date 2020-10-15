# -*- coding: utf-8 -*-
from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
from PyQt5.QtWidgets import QApplication, QLabel
from PositionFrame import PositionFrame
from ControlButtons import *
from NotificationsFrame import NotificationFrame
from StatusBar import StatusBar
from SerialArmController import SerialArmController
from datetime import datetime  # For log file formatting
import os.path
import webbrowser
import subprocess
import appscript  # added this


class Application(tk.Frame):
    '''The main GUI class'''
    counter = 0

    def __init__(self, master, **kwargs):
        '''
        The constructor for the Application class
        :param master: the Tk parent widget
        '''

        super().__init__(master, **kwargs)

        self.pack()
        self.taskbar_icon = tk.PhotoImage(file="SBLogo.png")
        self.master.call('wm', 'iconphoto', self.master._w, self.taskbar_icon)
        self.config(padx=16, pady=16)

        now = datetime.now()  # Create unique logfile for notifications and errors
        timestamp = now.strftime("%m_%d_%Y_%H_%M_%S")
        file_name = 'LOGFILE_' + timestamp + '.txt'
        self.logFile = open(os.path.join(os.path.realpath('../logs/'), file_name), 'w+')  # Save logfile to log folder

        # need the status bar to give to the arm controller
        self.status_bar = StatusBar(self)
        self.notifications_frame = NotificationFrame(self, self.logFile)

        self.serial_arm_controller = SerialArmController(self.status_bar, self.notifications_frame)

        self.create_widgets()

        # self.button = tk.Button(self, text="Create new window",
        #                         command=self.create_window)
        # self.button.pack(side="right")

    def create_window(self):
        self.counter += 1
        app = QApplication([])
        command = "python3 -m guiscrcpy"
        # os.system("python3 -m guiscrcpy")
        appscript.app('Terminal').do_script(command)
        # p = subprocess.Popen(command,shell=True)
        # p.wait()
        app.exec_()

    def create_widgets(self):
        '''Creates the widgets seen in the GUI'''

        self.menu_bar = tk.Menu(self)
        self.create_menu(self.menu_bar)

        self.position_frame = PositionFrame(self, self.serial_arm_controller, self.logFile)
        self.position_frame.pack(fill="x")

        self.control_buttons = ControlButtons(self, self.serial_arm_controller, self.notifications_frame)
        self.control_buttons.pack(fill="x")

        self.notifications_frame.pack(fill="x")

        self.status_bar.pack(fill="x")

        self.master.config(menu=self.menu_bar)

    def close_app(self):  # Had to make new quit function to close file
        '''Closes the GUI application'''

        self.logFile.close()
        self.quit()

    def create_menu(self, root_menu):
        '''
        Creates the main GUI menu
        :param root_menu: The root menu (self.menu_bar) that is instantiated in create_widgets()
        '''

        # File Menu
        self.file_menu = tk.Menu(root_menu, tearoff=0)
        # self.file_menu.add_command(label="Preferences", command=self.hello)
        self.file_menu.add_command(label="Quit", command=self.close_app)
        root_menu.add_cascade(label="File", menu=self.file_menu)

        # Device Menu
        self.device_menu = tk.Menu(root_menu, tearoff=0)

        self.device_menu.add_command(label="Refresh Devices", command=self.refresh_devices)
        self.device_menu.add_separator()

        root_menu.add_cascade(label="Device", menu=self.device_menu)

        # Help Menu
        self.help_menu = tk.Menu(root_menu, tearoff=0)
        self.help_menu.add_command(label="About Survivor Buddy 3.0", command=self.open_survivor_buddy_page)
        self.help_menu.add_command(label="User Manual", command=self.open_user_manual)
        self.help_menu.add_command(label="Programmer's Reference", command=self.open_programmer_reference)
        root_menu.add_cascade(label="Help", menu=self.help_menu)

    def refresh_devices(self):
        '''Refreshes the Devices menu'''

        self.device_menu.delete(2, 100)
        self.serial_arm_controller.update_devs()
        if not self.serial_arm_controller.devs:
            self.device_menu.add_command(label="No devices", state=tk.DISABLED)
        else:
            for dev in self.serial_arm_controller.devs:
                self.device_menu.add_command(
                    label="{}: {}".format(dev[0], dev[1]),
                    command=lambda: self.connect(dev)
                )

    def connect(self, dev):
        '''
        Connects to the given device
        :param dev: The serial device to connect to
        '''

        self.serial_arm_controller.connect(dev[0])
        self.device_menu.add_command(
            label="Close Connection",
            command=self.close
        )

    def close(self):
        '''Closes the active serial connection'''

        self.device_menu.delete(2 + len(self.serial_arm_controller.devs))
        self.serial_arm_controller.close()

    def open_survivor_buddy_page(self):
        webbrowser.open("http://survivorbuddy.cse.tamu.edu/")

    def open_user_manual(self):
        webbrowser.open(
            "https://docs.google.com/document/d/1V6gmVehsxrlFoc5FzThtdTNSovUbyU03AUEBfnAclKA/edit?usp=sharing")

    def open_programmer_reference(self):
        webbrowser.open("https://drive.google.com/a/tamu.edu/file/d/1pMKci4BTCTu7H6GREmmWEmBEgZ4klQWn/view?usp=sharing")

    def hello(self):
        '''
        A test function
        Simply prints "Hello from Menu" to the console and the NotificationsFrame
        '''
        print("Hello from Menu")
        self.notifications_frame.append_line("Hello from Menu")


def create_window():
    app = QApplication([])
    command = "python3 -m guiscrcpy"
    # os.system("python3 -m guiscrcpy")
    appscript.app('Terminal').do_script(command)
    # p = subprocess.Popen(command,shell=True)
    # p.wait()
    app.exec_()


if __name__ == "__main__":
    root = Tk()
    root.geometry("1000x800")
    # now = datetime.now()  # Create unique logfile for notifications and errors
    # timestamp = now.strftime("%m_%d_%Y_%H_%M_%S")
    # file_name = 'LOGFILE_' + timestamp + '.txt'
    # logFile = open(os.path.join(os.path.realpath('../logs/'), file_name), 'w+')

    # declaration of everything
    app = Application(master=root)
    # diagram_frame = Frame(root, height = 300, width = 700, highlightbackground="black", highlightthickness=1)
    # diagram_frame.place(x=50,y=100)
    # app.position_frame.place(in_=diagram_frame, anchor = CENTER, relx = 0.5, rely=0.1)
    # status_bar = StatusBar(master=root)
    # notifications_frame = NotificationFrame(master = root,_logFile=logFile)
    # serial_arm_controller = SerialArmController(status_bar, notifications_frame)
    # menu_bar = tk.Menu()
    # app.create_menu(menu_bar)
    # position_frame = PositionFrame(master = root,arm_controller=serial_arm_controller, _logFile=logFile)

    button = Button(root, text="Create new window",
                    command=create_window)
    button.place(x=500, y=700)

    # bottom right buttons
    # button_frame = Frame(root, height=245, width=150, highlightbackground="black", highlightthickness=1)
    # button_frame.place(x=825, y=530)
    # portrait_button = Button(button_frame, text="Portrait").place(in_=button_frame, anchor=CENTER, relx=0.5,
    #                                                                          rely=0.125)
    # landscape_button = Button(button_frame, text="Landscape").place(in_=button_frame, anchor=CENTER, relx=0.5,
    #                                                               rely=0.25)
    # open_arm_button = Button(button_frame, text="Open Arm").place(in_=button_frame, anchor=CENTER, relx=0.5,
    #                                                               rely=0.375)
    # close_arm_button = Button(button_frame, text="Close Arm").place(in_=button_frame, anchor=CENTER, relx=0.5,
    #                                                               rely=0.5)
    # tilt_head_button = Button(button_frame, text="Tilt Head").place(in_=button_frame, anchor=CENTER, relx=0.5,
    #                                                               rely=0.625)
    # nod_head_button = Button(button_frame, text="Nod Head").place(in_=button_frame, anchor=CENTER, relx=0.5,
    #                                                               rely=0.75)
    # shake_head_button = Button(button_frame, text="Shake Head").place(in_=button_frame, anchor=CENTER, relx=0.5,
    #                                                               rely=0.875)

    app.master.title("Survivor Buddy 3.0")
    root.protocol("WM_DELETE_WINDOW", app.close_app)
    app.mainloop()