from tkinter import *
from Phidget22.Devices.DCMotor import *
from Phidget22.Devices.CurrentInput import *
from Phidget22.Devices.VoltageRatioInput import *
from Phidget22.Devices.DigitalOutput import *
from Phidget22.Devices.VoltageOutput import *
from Phidget22.Net import *
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

#Max/Min Pressure of Regulator Input
MAXPR = 130.5
MINPR = 0.5

#Serial Numbers for Devices
HUB1 = 539685
HUB2 = 538463
INTER = 527272
#Solenoids
CH1_S = [HUB2, 5, 1]
CH2_S = [HUB2, 5, 2]
CH3_S = [HUB2, 5, 3]
CH4_S = [HUB2, 5, 4]
CH5_S = [HUB2, 5, 5]
#Regulator Power
CH1_RP = [HUB2, 5, 11]
CH2_RP = [HUB2, 5, 12]
CH3_RP = [HUB2, 5, 13]
CH4_RP = [HUB2, 5, 14]
CH5_RP = [HUB2, 5, 15]
#Regulator Set Pressure
CH1_RSP = [HUB1, 0, 0]
CH2_RSP = [HUB1, 1, 0]
CH3_RSP = [HUB1, 2, 0]
CH4_RSP = [HUB1, 3, 0]
CH5_RSP = [HUB1, 4, 0]
#Regulator Observed Pressure
CH1_ROP = [INTER, 0]
CH2_ROP = [INTER, 1]
CH3_ROP = [INTER, 2]
CH4_ROP = [INTER, 3]
CH5_ROP = [INTER, 4]

#Line required to look for Phidget devices on the network
Net.enableServerDiscovery(PhidgetServerType.PHIDGETSERVER_DEVICEREMOTE)

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
    def __init__(self, master, initial_name, color, sol, reg_pwr, reg_set, reg_get):
        frame = Frame(master, borderwidth=2, relief=SUNKEN, bg=color)
        frame.pack()
        self.master = master
        self.frame_name = StringVar()
        self.frame_name.set(initial_name)
        self.state = 0
        self.fontType = "Comic Sans"
        self.activeColor = 'SpringGreen4'

        self.pressure = IntVar()
        self.pressure.set("")

        self.power = Button(frame, text="PWR", activebackground=self.activeColor, command=lambda: self.toggle_pwr())
        self.extend = Button(frame, text="EXTEND", bg=self.activeColor, activebackground=self.activeColor, state=DISABLED, command=lambda: self.solenoid_extend())
        self.retract = Button(frame, text="RETRACT", activebackground=self.activeColor, state=DISABLED, command=lambda: self.solenoid_retract())
        self.set_label = Button(frame, text="SET LABEL", font=(self.fontType,7), command=lambda: self.get_label_input())
        self.observed_pressure = Entry(frame, width=5, state="readonly", textvariable = self.pressure)
        self.set_pressure = Scale(frame, orient=HORIZONTAL, from_=0, to=130.5, resolution=0.5, bg=color, label="Set Pressure (PSI)", highlightthickness=0, command= self.set_pressure)
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

        # Connect to Phidget Solid State Relay for solinoid control
        self.soldnoid_switch = DigitalOutput()
        self.soldnoid_switch.setDeviceSerialNumber(sol[0])
        self.soldnoid_switch.setIsHubPortDevice(False)
        self.soldnoid_switch.setHubPort(sol[1])
        self.soldnoid_switch.setChannel(sol[2])
        self.soldnoid_switch.openWaitForAttachment(5000)

        #Connect to Phidget Solid State Relay for regulator power control
        self.reg_switch = DigitalOutput()
        self.reg_switch.setDeviceSerialNumber(reg_pwr[0])
        self.reg_switch.setIsHubPortDevice(False)
        self.reg_switch.setHubPort(reg_pwr[1])
        self.reg_switch.setChannel(reg_pwr[2])
        self.reg_switch.openWaitForAttachment(5000)

        #Connect to Phidget Voltage Ouptut for pressure control
        self.pressure_ctrl = VoltageOutput()
        self.pressure_ctrl.setDeviceSerialNumber(reg_set[0])
        self.pressure_ctrl.setIsHubPortDevice(False)
        self.pressure_ctrl.setHubPort(reg_set[1])
        self.pressure_ctrl.setChannel(reg_set[2])
        self.pressure_ctrl.openWaitForAttachment(5000)

        #Connect to Phidget Analog Input for pressure reading
        self.pressure_reading = VoltageRatioInput()
        self.pressure_reading.setDeviceSerialNumber(reg_get[0])
        self.pressure_reading.setChannel(reg_get[1])
        self.pressure_reading.openWaitForAttachment(5000)

    def toggle_pwr(self):
        #Turn on air channel
        if self.state == 0:
            #Turn on power to regulator and show active button color
            self.power.config(bg=self.activeColor)
            self.reg_switch.setState(True)

            #Enable Extend and Retract buttons
            self.extend.config(state=NORMAL)
            self.retract.config(state=NORMAL)

            #Start monitoring air pressure
            self.update_pressure()

            #Change state of air channel
            self.state = 1

        #Turn off air channel
        elif self.state == 1:
            # Change pressure to zero
            self.set_pressure.set(0)
            self.reg_switch.setState(False)

            #Turn off power to reguluator and remove active button color
            self.power.config(bg="SystemButtonFace")

            #Turn off power to solenoid which changes the state to Extend, disable buttons
            self.extend.config(state=DISABLED, bg=self.activeColor)
            self.retract.config(state=DISABLED, bg="SystemButtonFace")
            self.solenoid_extend()

            #Update air channel state
            self.state = 0

    def solenoid_retract(self):
        self.extend.config(bg="SystemButtonFace")
        self.retract.config(bg=self.activeColor)
        self.soldnoid_switch.setState(True)

    def solenoid_extend(self):
        self.retract.config(bg="SystemButtonFace")
        self.extend.config(bg=self.activeColor)
        self.soldnoid_switch.setState(False)

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
    def set_pressure(self, val):
        # Pressure Range
        range = MAXPR - MINPR
        # Calculate volts/PSI
        ratio = 5 / range
        self.pressure_ctrl.setVoltage(float(val) * ratio)

    def update_pressure(self):
        if self.reg_switch.getState():
            try:
                val = float(self.pressure_reading.getSensorValue())
                PSI = val * 160.5 - 30.5
                self.pressure.set(round(PSI, 2))
            except:
                print("Init Air Pressure")
            root.after(100, self.update_pressure)
        else:
            self.pressure.set("")

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
        frame4.grid(row=1, column=0)
        frame5.grid(row=1, column=1)
        frame6.grid(row=1, column=2)

        out1 = PneumaticFrame(frame1, "Channel #1", colorArray[0], CH1_S, CH1_RP, CH1_RSP, CH1_ROP)
        out2 = PneumaticFrame(frame2, "Channel #2", colorArray[1], CH2_S, CH2_RP, CH2_RSP, CH2_ROP)
        out3 = PneumaticFrame(frame3, "Channel #3", colorArray[2], CH3_S, CH3_RP, CH3_RSP, CH3_ROP)
        out4 = PneumaticFrame(frame4, "Channel #4", colorArray[3], CH4_S, CH4_RP, CH4_RSP, CH4_ROP)
        out5 = PneumaticFrame(frame5, "Channel #5", colorArray[4], CH5_S, CH5_RP, CH5_RSP, CH5_ROP)
        #out6 = PneumaticFrame(frame6, "Channel #6", colorArray[5])



root = Tk()
TIMC = MainWindow(root, SetupMainWindow())
root.mainloop()
