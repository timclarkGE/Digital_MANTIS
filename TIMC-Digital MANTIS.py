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
        self.gui_height = 555

class MainWindow:
    def __init__(self, master, parameters):
        self.parameters = parameters
        self.master = master
        self.master.geometry(str(parameters.gui_width) + "x" + str(parameters.gui_height))
        self.master.title("Tooling Inspection Motion Controller - Digital MANTIS")

        #Create Frame for Pnematics Control
        self.out1 = AxisControlFrame(self.master, blue_checkers)

        #class CameraFrame:

        #class AxisFrame:

class popupWindow(object):
    def __init__(self, master, current_limit):
        self.limit = StringVar()
        top=self.top=Toplevel(master)
        self.current_limit = Entry(top, width=5, textvariable = self.limit)
        self.limit.set(current_limit)
        self.label_current_limit = Label(top, text="Current Limit (A) Range: 2 to 25")
        self.max_velocity = Entry(top, width=5)
        self.label_max_velocity = Label(top, text="Max Velocity Percentage, Range: 1 to 100")
        self.acceleration = Entry(top, width=5)
        self.label_acceleration = Label(top, text="Acceleration, Range 0.1 to 100")
        self.apply = Button(top, text="APPLY", command=self.check_data)
        self.current_limit.grid(row=0, column=0)
        self.label_current_limit.grid(row=0, column=1, stick=W)
        self.max_velocity.grid(row=1, column=0)
        self.label_max_velocity.grid(row=1, column=1, sticky=W)
        self.acceleration.grid(row=2, column=0)
        self.label_acceleration.grid(row=2, column=1, sticky=W)
        self.apply.grid(row=5,column=0)

    def check_data(self):
        if self.current_limit.get().isdigit():
            if float(self.current_limit.get())>0:
                print("Good Job")
                self.cleanup()
        else:
            messagebox.showerror("Idiot", "Current Limit must be a number Stupid")

    def cleanup(self):

        self.value = self.current_limit.get()
        self.top.destroy()

class AxisFrame:
    def __init__(self, master, initial_name, color):
        frame = Frame(master, borderwidth=2, relief=SUNKEN, bg=color)
        frame.pack()
        self.master = master
        self.frame_name = StringVar()
        self.frame_name.set(initial_name)
        self.fontType = "Comic Sans"
        self.activeColor = 'SpringGreen4'

        #Needed?
        self.current_limit = 2
        # self.max_velocity
        # self.acceleration
        # self.invert
        # self.holding_voltage
        # self.axis_name
        # self.bulkhead_number
        # self.move_pos_text
        # self.move_neg_text

        self.jog_pos_btn = Button(frame, text="POSITIVE", command=lambda: self.jog("+"))
        self.jog_neg_btn = Button(frame, text="NEGATIVE", command=lambda: self.jog("-"))
        self.config = Button(frame, text="CONFIGURE AXIS", font=(self.fontType,6), command=lambda: self.get_label_input())
        self.current = Entry(frame, width=5, state=DISABLED)
        self.speed = Scale(frame, orient=HORIZONTAL, from_=0.01, to=1, resolution=.01, bg=color, label="      Axis Speed", highlightthickness=0)
        self.custom_label = Label(frame, textvariable=self.frame_name, font=(self.fontType, 14), bg=color)
        self.label = Label(frame, text=initial_name, bg=color)

        frame.rowconfigure(0, minsize=30)
        self.custom_label.grid(row=0, column=0, columnspan=2, sticky=S)
        self.jog_pos_btn.grid(column=0, row=1, pady=10)
        self.jog_neg_btn.grid(column=0, row=2, pady=10)
        self.current.grid(column=0, row=3,pady=5)
        self.speed.grid(column=0, row=4, padx=20)
        self.config.grid(column=0, row=5, pady=5)
        self.label.grid(column=0, row=6)

    def jog(self, direction):
        print("JOGGING "+direction)

    def get_label_input(self):
        self.window = popupWindow(self.master, self.current_limit)
        self.config.config(state=DISABLED)
        self.master.wait_window(self.window.top)
        self.config.config(state=NORMAL)

        #If the user does not enter a value exception will be produced
        try:
            if len(self.window.value)>12:
                self.frame_name.set("SET ERROR")
            else:
                self.frame_name.set(self.window.value)
        except:
            self.frame_name.set("SET ERROR")

class AxisControlFrame:
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
        frame6.grid(row=0, column=5)
        frame7.grid(row=0, column=6)


        out1 = AxisFrame(frame1, "Channel #1", colorArray[0])
        out2 = AxisFrame(frame2, "Channel #2", colorArray[1])
        out3 = AxisFrame(frame3, "Channel #3", colorArray[2])
        out4 = AxisFrame(frame4, "Channel #4", colorArray[3])
        out5 = AxisFrame(frame5, "Channel #5", colorArray[4])
        out6 = AxisFrame(frame6, "Channel #6", colorArray[5])
        out7 = AxisFrame(frame7, "Channel #7", colorArray[6])
        out8 = AxisFrame(frame8, "Channel #8", colorArray[7])
        out9 = AxisFrame(frame9, "Channel #9", colorArray[8])
        out10 = AxisFrame(frame10, "Channel #10", colorArray[9])

root = Tk()
TIMC = MainWindow(root, SetupMainWindow())
root.mainloop()
