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

    def connect(self, text):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect(self.full_addr)
        except ConnectionRefusedError:
            newWindow=Toplevel(self.master)
            newWindow.geometry("600x50")
            newWindow.title("Error Message")
            label = Label(newWindow, text= 'Your text: "'+ text+ '" could not sent\nError Message: Please open Show Messages in Survivor Buddy Mobile App')
            label.pack()
            print("Could not send message: Please open Show Messages in Survivor Buddy Mobile App")
            return False

        except TimeoutError:
            newWindow = Toplevel(self.master)
            newWindow.geometry("600x50")
            newWindow.title("Error Message")
            label = Label(newWindow, text='Your text: "'+ text+ '" could not sent\nError Message: Ensure that the ip address and port number are correct')
            label.pack()
            print("Connection to Mobile Device Timed out: Ensure that the ip address and port number are correct")
            return False

        return True
        

    def disconnect(self):
        self.client_socket.close()

    def sendMsg(self, msg_str):
        threading.Thread(target=self.handleSend, args=(msg_str,)).start()

    def handleSend(self, msg_str):
        if self.connect(msg_str):
            self.client_socket.sendall(msg_str.encode(self.str_format))
            self.disconnect()





