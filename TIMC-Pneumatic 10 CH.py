from tkinter import *
from tkinter import messagebox
import threading
import queue
import time
import datetime
import platform
import sys

rainbow = ['SteelBlue1', 'DarkGoldenrod1', 'PaleGreen3','LightBlue3','DarkSlateGray3', 'MistyRose3','LightYellow3', 'dark khaki', 'LightSalmon2', 'chocolate1']
blue_checkers = ['LightSkyBlue1', 'LightSkyBlue3','LightSkyBlue1', 'LightSkyBlue3','LightSkyBlue1', 'LightSkyBlue3','LightSkyBlue1', 'LightSkyBlue3','LightSkyBlue1', 'LightSkyBlue3']
green_checkers = ['DarkOliveGreen1', 'DarkOliveGreen4','DarkOliveGreen1', 'DarkOliveGreen4','DarkOliveGreen1', 'DarkOliveGreen4','DarkOliveGreen1', 'DarkOliveGreen4','DarkOliveGreen1', 'DarkOliveGreen4']
green_checkers2 = ['DarkOliveGreen3', 'DarkOliveGreen4','DarkOliveGreen3', 'DarkOliveGreen4','DarkOliveGreen3', 'DarkOliveGreen4','DarkOliveGreen3', 'DarkOliveGreen4','DarkOliveGreen3', 'DarkOliveGreen4']
gold_checkers = ['gold2', 'gold3','gold2', 'gold3','gold2', 'gold3','gold2', 'gold3','gold2', 'gold3',]
orange_checkers = ['DarkOrange2', 'DarkOrange4','DarkOrange2', 'DarkOrange4','DarkOrange2', 'DarkOrange4','DarkOrange2', 'DarkOrange4','DarkOrange2', 'DarkOrange4',]

class SetupMainWindow:
    def __init__(self):
        self.gui_width = 750
        self.gui_height = 470

class MainWindow:
    def __init__(self, master, parameters):
        self.parameters = parameters
        self.master = master
        self.master.geometry(str(parameters.gui_width) + "x" + str(parameters.gui_height))
        self.master.title("Tooling Inspection Motion Controller - Pneumatic 10 CH")

        #Create Frame for Pneumatics Control
        self.out1 = PneumaticControlFrame(self.master, blue_checkers)

        #class CameraFrame:

        #class AxisFrame:

class popupWindow(object):
    def __init__(self, master):
        top=self.top=Toplevel(master)
        self.prompt = Label(top, text="Enter Name")
        self.prompt.pack()
        self.warning = Label(top, text="(Max 12 Characters)")
        self.warning.pack()
        self.entry = Entry(top, width=12)
        self.entry.pack()
        self.entry.focus()
        self.apply = Button(top, text="APPLY", command=self.cleanup)
        self.apply.pack()

    def cleanup(self):
        self.value = self.entry.get()
        self.top.destroy()

class PneumaticFrame:
    def __init__(self, master, initial_name, color):
        frame = Frame(master, borderwidth=2, relief=SUNKEN, bg=color)
        frame.pack()
        self.master = master
        self.frame_name = StringVar()
        self.frame_name.set(initial_name)
        self.state = 0
        self.fontType = "Comic Sans"
        self.activeColor = 'SpringGreen4'


        self.power = Button(frame, text="PWR", activebackground=self.activeColor, command=lambda: self.toggle_pwr())
        self.extend = Button(frame, text="EXTEND", bg=self.activeColor, activebackground=self.activeColor, state=DISABLED, command=lambda: self.solenoid_extend())
        self.retract = Button(frame, text="RETRACT", activebackground=self.activeColor, state=DISABLED, command=lambda: self.solenoid_retract())
        self.set_label = Button(frame, text="SET LABEL", font=(self.fontType,7), command=lambda: self.get_label_input())
        self.observed_pressure = Entry(frame, width=5)
        self.set_pressure = Scale(frame, orient=HORIZONTAL, from_=0.5, to=130.5, resolution=0.5, bg=color, label="Set Pressure (PSI)", highlightthickness=0)
        self.custom_label = Label(frame, textvariable=self.frame_name, font=(self.fontType, 14), bg=color)
        self.label = Label(frame, text=initial_name, bg=color)

        frame.rowconfigure(0, minsize=30)
        self.custom_label.grid(row=0, column=0, columnspan=2, sticky=S)
        self.set_label.grid(column=0, row=1, columnspan=2)
        frame.rowconfigure(2, minsize=50)
        self.power.grid(column=0, row=2)
        self.observed_pressure.grid(column=1, row=2)
        self.set_pressure.grid(column=0, row=3, columnspan=2, padx=20)
        frame.rowconfigure(4, minsize=50)
        self.extend.grid(column=0, row=4)
        self.retract.grid(column=1, row=4)
        self.label.grid(column=0, row=5, columnspan=2)

    def toggle_pwr(self):
        #Turn on air channel
        if self.state == 0:
            #Turn on power to regulator and show active button color
            self.power.config(bg=self.activeColor)

            #Enable Extend and Retract buttons
            self.extend.config(state=NORMAL)
            self.retract.config(state=NORMAL)

            #Change state of air channel
            self.state = 1

        #Turn off air channel
        elif self.state == 1:
            # Change pressure to zero
            self.set_pressure.set(0.5)

            #Turn off power to reguluator and remove active button color
            self.power.config(bg="SystemButtonFace")

            #Turn off power to solenoid which changes the state to Extend, disable buttons
            self.extend.config(state=DISABLED, bg=self.activeColor)
            self.retract.config(state=DISABLED, bg="SystemButtonFace")

            #Update air channel state
            self.state = 0

    def solenoid_retract(self):
        self.extend.config(bg="SystemButtonFace")
        self.retract.config(bg=self.activeColor)

    def solenoid_extend(self):
        self.retract.config(bg="SystemButtonFace")
        self.extend.config(bg=self.activeColor)

    def get_label_input(self):
        self.window = popupWindow(self.master)
        self.set_label.config(state=DISABLED)
        self.master.wait_window(self.window.top)
        self.set_label.config(state=NORMAL)

        #If the user does not enter a value exception will be produced
        try:
            if len(self.window.value)>12:
                self.frame_name.set("SET ERROR")
            else:
                self.frame_name.set(self.window.value)
        except:
            self.frame_name.set("SET ERROR")

class PneumaticControlFrame:
    def __init__(self, master, colorArray):
        frame1 = Frame(master, borderwidth=2, relief=SUNKEN)
        frame2 = Frame(master, borderwidth=2, relief=SUNKEN)
        frame3 = Frame(master, borderwidth=2, relief=SUNKEN)
        frame4 = Frame(master, borderwidth=2, relief=SUNKEN)
        frame5 = Frame(master, borderwidth=2, relief=SUNKEN)
        frame6 = Frame(master, borderwidth=2, relief=SUNKEN)
        frame7 = Frame(master, borderwidth=2, relief=SUNKEN)
        frame8 = Frame(master, borderwidth=2, relief=SUNKEN)
        frame9 = Frame(master, borderwidth=2, relief=SUNKEN)
        frame10 = Frame(master, borderwidth=2, relief=SUNKEN)

        frame1.grid(row=0,column=0)
        frame2.grid(row=0,column=1)
        frame3.grid(row=0, column=2)
        frame4.grid(row=0, column=3)
        frame5.grid(row=0, column=4)
        frame6.grid(row=1, column=0)
        frame7.grid(row=1, column=1)
        frame8.grid(row=1, column=2)
        frame9.grid(row=1, column=3)
        frame10.grid(row=1, column=4)

        out1 = PneumaticFrame(frame1, "Channel #1", colorArray[0])
        out2 = PneumaticFrame(frame2, "Channel #2", colorArray[1])
        out3 = PneumaticFrame(frame3, "Channel #3", colorArray[2])
        out4 = PneumaticFrame(frame4, "Channel #4", colorArray[3])
        out5 = PneumaticFrame(frame5, "Channel #5", colorArray[4])
        out6 = PneumaticFrame(frame6, "Channel #6", colorArray[5])
        out7 = PneumaticFrame(frame7, "Channel #7", colorArray[6])
        out8 = PneumaticFrame(frame8, "Channel #8", colorArray[7])
        out9 = PneumaticFrame(frame9, "Channel #9", colorArray[8])
        out10 = PneumaticFrame(frame10, "Channel #10", colorArray[9])


root = Tk()
TIMC = MainWindow(root, SetupMainWindow())
root.mainloop()
