import serial 
from tkinter import *

window = Tk()
 
window.title("Survior Buddy 3.0")
window.geometry('450x300')

#Used with motorMovement arduino
arduinoData = serial.Serial('com5',9600)

def motor_zero():
	arduinoData.write(str.encode('0')) 
	print("motor_zero pressed")

def motor_port():
	arduinoData.write(str.encode('1'))
	print("motor_port pressed")

def motor_lands():
	arduinoData.write(str.encode('2'))
	print("motor lands pressed")

def motor_left():
	arduinoData.write(str.encode('3'))
	print("motor left pressed")

def motor_right():
	arduinoData.write(str.encode('4'))
	print("motor right pressed")

def motor_leftBM():
	arduinoData.write(str.encode('5'))
	print("motor leftBM pressed")

def motor_rightBM():
	arduinoData.write(str.encode('6'))
	print("motor rightBM pressed")

def motor_base180():
	arduinoData.write(str.encode('7'))
	print("motor base 180 pressed")

def nod():
	arduinoData.write(str.encode('8'))
	print("nod pressed")

phoneServoLabel = Label(window,text='PhoneMount Controls')
phoneServoLabel.grid(column=5, row=0);

baseServoLabel = Label(window,text='Base Controls')
baseServoLabel.grid(column=7, row=0);

btn = Button(window, text="Motor Zero", command=motor_zero) 
btn.grid(column=5, row=1)

btn2 = Button(window, text="Motor Portrait", command=motor_port) 
btn2.grid(column=5, row=2)

btn3 = Button(window, text="Motor Landscape", command=motor_lands) 
btn3.grid(column=5, row=3)

btn4 = Button(window, text="Move left", command = motor_left)
btn4.grid(column=5,row=4)

btn5 = Button(window, text="Move right", command = motor_right)
btn5.grid(column=5,row=5)


btn6 = Button(window, text="Move left", command = motor_leftBM)
btn6.grid(column=7,row=4)

btn7 = Button(window, text="Move right", command = motor_rightBM)
btn7.grid(column=7,row=5)

btn8 = Button(window, text="180 pos", command = motor_base180)
btn8.grid(column=7,row=6)

btn9 = Button(window, text="Nod", command = nod)
btn9.grid(column=7,row=7)


window.mainloop()

input("Press enter to exit")