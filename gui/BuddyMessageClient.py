import socket
import threading
from tkinter import *
from tkinter.ttk import *

class BuddyMessageClient:

    def __init__(self, server_ip, port_num, master, str_format='utf-8'):

        self.server_ip = server_ip
        self.port_num = port_num
        self.full_addr = (self.server_ip, self.port_num)
        self.str_format = str_format
        self.client_socket = None
        self.master = master

    def show_error(self, error_msg):
        if(self.master is not None):
            newWindow = Toplevel(self.master)
            newWindow.geometry("600x50")
            newWindow.title("Error Message")
            label = Label(newWindow, text= error_msg)
            label.pack()

    def connect(self, text="DEFAULT_MESSAGE"):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect(self.full_addr)
            return True

        except ConnectionRefusedError:
            self.show_error("Error Message: Connection Refused")
            return False

        except TimeoutError:
            self.show_error("Error Message: Connection TimedOut")
            return False

        return None

    def disconnect(self):
        if(self.client_socket is not None):
            self.client_socket.close()
            self.client_socket = None

    def sendMsg(self, msg_str):
        threading.Thread(target=self.handleSend, args=(msg_str,)).start()

    def handleSend(self, msg_str):
        if self.connect(msg_str):
            self.client_socket.sendall(msg_str.encode(self.str_format))
            self.disconnect()