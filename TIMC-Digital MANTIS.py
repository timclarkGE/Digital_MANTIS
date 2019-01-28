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
        self.gui_width = 1050
        self.gui_height = 555

class MainWindow:
    def __init__(self, master, parameters):
        self.parameters = parameters
        self.master = master
        self.master.geometry(str(parameters.gui_width) + "x" + str(parameters.gui_height))
        self.master.title("Tooling Inspection Motion Controller - Digital MANTIS Electrical")

        #Create Frame for Pnematics Control
        self.out1 = AxisControlFrame(self.master, blue_checkers)

        #class CameraFrame:

        #class AxisFrame:

class popupWindow(object):
    def __init__(self, master, current_limit, max_velocity, acceleration, invert):
        top = self.top = Toplevel(master)

        self.invert = BooleanVar()
        self.invert.set(invert)

        self.scale_current_limit = Scale(top, orient=HORIZONTAL, from_=2, to=25, resolution=.1,
                           label="Current Limit (A)", length=200)
        self.scale_max_velocity = Scale(top, orient=HORIZONTAL, from_=1, to=100, resolution=1,
                           label="Max Velocity (%)", length=200)
        self.scale_acceleration = Scale(top, orient=HORIZONTAL, from_=0.1, to=100, resolution=0.1,
                           label="Max Acceleration (dty/s^2)", length=200)
        self.ckbx_invert = Checkbutton(top, text="Invert Axis Direction", variable=self.invert)
        self.btn_apply = Button(top, text="APPLY", command=self.apply_data)

        #Init the window to the current settings
        self.scale_current_limit.set(current_limit)
        self.scale_max_velocity.set(max_velocity*100)
        self.scale_acceleration.set(acceleration)

        #Grid the widgets
        self.scale_current_limit.grid(row=0, column=0, stick=W)
        self.scale_max_velocity.grid(row=1, column=0, sticky=W)
        self.scale_acceleration.grid(row=2, column=0, sticky=W)
        self.ckbx_invert.grid(row=3, column=0)
        self.btn_apply.grid(row=4,column=0)

    def apply_data(self):
        self.current_limit = self.scale_current_limit.get()
        self.max_velocity = self.scale_max_velocity.get()/100
        self.acceleration = self.scale_acceleration.get()
        self.cleanup()

    def cleanup(self):
        self.top.destroy()

class AxisFrame:
    def __init__(self, master, initial_name, color):
        frame = Frame(master, borderwidth=2, relief=SUNKEN, bg=color)
        frame.pack()
        self.master = master
        self.frame_name = StringVar()
        self.frame_name.set(initial_name)
        self.fontType = "Comic Sans"

        #Set the parameters for the axis
        self.current_limit = 5          #2 to 25A
        self.max_velocity = 1           #0 to 1
        self.acceleration = 0.1         #0.1 to 100
        self.invert = FALSE             #TRUE or FALSE
        self.axis_name = initial_name
        self.bulkhead_number = 1        #TODO, need to set this as a variable
        self.move_pos_text  = "POSITIVE"
        self.move_neg_text = "NEGATIVE"

        self.jog_pos_btn = Button(frame, text=self.move_pos_text, command=lambda: self.jog("+"))
        self.jog_neg_btn = Button(frame, text=self.move_neg_text, command=lambda: self.jog("-"))
        self.configure_btn = Button(frame, text="CONFIGURE", font=(self.fontType,6), command=lambda: self.configure())
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
        self.configure_btn.grid(column=0, row=5, pady=5)
        self.label.grid(column=0, row=6)

    def jog(self, direction):
        print("JOGGING "+direction)

    def configure(self):
        #current_limit, max_velocity, acceleration, invert
        self.window = popupWindow(self.master, self.current_limit, self.max_velocity, self.acceleration, self.invert)
        self.configure_btn.config(state=DISABLED)
        self.master.wait_window(self.window.top)
        self.configure_btn.config(state=NORMAL)

        #Set the new parameters from the configuration window
        self.current_limit = self.window.current_limit
        self.max_velocity = self.window.max_velocity
        self.acceleration = self.window.acceleration
        self.invert = self.window.invert.get()

        print(self.current_limit, self.max_velocity, self.acceleration, self.invert)
        #Get the users information and update the axis information: current limit, max speed, acceleration, invert
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

        frame1.grid(row=0,column=0)
        frame2.grid(row=0,column=1)
        frame3.grid(row=0, column=2)
        frame4.grid(row=0, column=3)
        frame5.grid(row=0, column=4)
        frame6.grid(row=0, column=5)
        frame7.grid(row=0, column=6)


        out1 = AxisFrame(frame1, "BASE CIRC", colorArray[0])
        out2 = AxisFrame(frame2, "BASE AUX", colorArray[1])
        out3 = AxisFrame(frame3, "VARD VERT", colorArray[2])
        out4 = AxisFrame(frame4, "VARD ROT", colorArray[3])
        out5 = AxisFrame(frame5, "DA MAST", colorArray[4])
        out6 = AxisFrame(frame6, "DA PAN", colorArray[5])
        out7 = AxisFrame(frame7, "DA TILT", colorArray[6])


root = Tk()
TIMC = MainWindow(root, SetupMainWindow())
root.mainloop()
