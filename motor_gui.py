import serial 
from tkinter import *

window = Tk()
 
window.title("Survior Buddy 3.0")
window.geometry('450x300')

#Used with sweeper_test
arduinoData = serial.Serial('com5',9600)

def motor_cw():
	arduinoData.write(str.encode('1')) 
	print("motor_cw pressed")

def motor_ccw():
	arduinoData.write(str.encode('0'))
	print("motor_ccw pressed")

def motor_stop():
	arduinoData.write(str.encode('2'))
	print("motor stop pressed")

btn = Button(window, text="Motor CW", command=motor_cw) 
btn.grid(column=5, row=1)

btn2 = Button(window, text="Motor CCW", command=motor_ccw) 
btn2.grid(column=5, row=2)

btn3 = Button(window, text="Motor Stop", command=motor_stop) 
btn3.grid(column=5, row=3)

window.mainloop()

input("Press enter to exit")