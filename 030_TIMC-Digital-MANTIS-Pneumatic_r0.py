###################################################################
# Tooling Inspection Motion Controller - Digital MANTIS Pneumatic #
#
# Author: Timothy Clark
# Email: timothy.clark@ge.com
# Date: 2/14/2019
# Code Revision: 0
#
# Description:
#   This code runs the Digital MANTIS system which is composed of
# multiple pneumatic channels. Channels 1-6 and Hydro utilize a solenoid
# The purge channels do not use a solenoid. Mechanical relays provide power
# to the pressure regulators, and the solenoids are controlled by solid
# state relays.

from tkinter import *
from Phidget22.Devices.VoltageRatioInput import *
from Phidget22.Devices.DigitalOutput import *
from Phidget22.Devices.VoltageOutput import *
from Phidget22.Net import *
from tkinter import messagebox
import time

rainbow = ['SteelBlue1', 'DarkGoldenrod1', 'PaleGreen3','LightBlue3','DarkSlateGray3', 'MistyRose3','LightYellow3', 'dark khaki', 'LightSalmon2', 'chocolate1']
blue_checkers = ['LightSkyBlue1', 'LightSkyBlue3','LightSkyBlue1', 'LightSkyBlue3','LightSkyBlue1', 'LightSkyBlue3','LightSkyBlue1', 'LightSkyBlue3','LightSkyBlue1', 'LightSkyBlue3']
green_checkers = ['DarkOliveGreen1', 'DarkOliveGreen4','DarkOliveGreen1', 'DarkOliveGreen4','DarkOliveGreen1', 'DarkOliveGreen4','DarkOliveGreen1', 'DarkOliveGreen4','DarkOliveGreen1', 'DarkOliveGreen4']
green_checkers2 = ['DarkOliveGreen3', 'DarkOliveGreen4','DarkOliveGreen3', 'DarkOliveGreen4','DarkOliveGreen3', 'DarkOliveGreen4','DarkOliveGreen3', 'DarkOliveGreen4','DarkOliveGreen3', 'DarkOliveGreen4']
gold_checkers = ['gold2', 'gold3','gold2', 'gold3','gold2', 'gold3','gold2', 'gold3','gold2', 'gold3',]
orange_checkers = ['DarkOrange2', 'DarkOrange4','DarkOrange2', 'DarkOrange4','DarkOrange2', 'DarkOrange4','DarkOrange2', 'DarkOrange4','DarkOrange2', 'DarkOrange4',]

#Max/Min Pressure of Regulator Input
MAXPR = 130.5 #Default maximum pressure of the ITV1050-21N2BL4 Pressure regulator
MINPR = 0.0

#System A
SN = "030"
HUB1 = 538774
HUB2 = 538780
SBCH = 512907
INTER = 527456  #interface kit 8/8/8

#Serial Numbers for Devices
#System B
#SN = "031"
#HUB1 = 539685
#HUB2 = 538463
#SBCH = 512770
#INTER = 527455  #interface kit 8/8/8

#System C
#SN = "032"
#HUB1 = 539540
#HUB2 = 539115
#SBCH = 512844
#INTER = 527447  #interface kit 8/8/8

#Solenoids
CH1_S = [HUB2, 0, 1]
CH2_S = [HUB2, 0, 2]
CH3_S = [HUB2, 0, 3]
CH4_S = [HUB2, 0, 4]
CH5_S = [HUB2, 0, 5]
CH6_S = [HUB2, 0, 6]
HYD_S = [HUB2, 0, 7]
#Regulator Power
CH1_RP = [SBCH, 4, 3]
CH2_RP = [SBCH, 4, 2]
CH3_RP = [SBCH, 5, 1]
CH4_RP = [SBCH, 5, 0]
CH5_RP = [SBCH, 3, 3]
CH6_RP = [SBCH, 4, 0]
PG1_RP = [SBCH, 5, 2]
PG2_RP = [SBCH, 4, 1]
HYD_RP = [SBCH, 5, 3]
#Regulator Set Pressure
CH1_RSP = [HUB1, 4, 0]
CH2_RSP = [HUB1, 5, 0]
CH3_RSP = [HUB2, 3, 0]
CH4_RSP = [HUB2, 4, 0]
CH5_RSP = [HUB2, 5, 0]
CH6_RSP = [HUB1, 3, 0]
PG1_RSP = [HUB1, 1, 0]
PG2_RSP = [HUB1, 2, 0]
HYD_RSP = [HUB1, 0, 0]

#Regulator Observed Pressure
CH1_ROP = [INTER, 4]
CH2_ROP = [INTER, 5]
CH3_ROP = [INTER, 6]
CH4_ROP = [INTER, 7]
CH5_ROP = [SBCH, 0]
CH6_ROP = [INTER, 3]
PG1_ROP = [INTER, 1]
PG2_ROP = [INTER, 2]
HYD_ROP = [INTER, 0]

#Line required to look for Phidget devices on the network
Net.enableServerDiscovery(PhidgetServerType.PHIDGETSERVER_DEVICEREMOTE)

class SetupMainWindow:
    def __init__(self):
        self.gui_width = 450
        self.gui_height = 695

class MainWindow:
    def __init__(self, master, parameters):
        self.parameters = parameters
        self.master = master
        self.master.geometry(str(parameters.gui_width) + "x" + str(parameters.gui_height))
        self.master.title("R0 - TIMC Digital MANTIS Pneumatic - S/N: "+ SN)

        #Create Frame for Pneumatics Control
        self.out1 = PneumaticControlFrame(self.master, blue_checkers)

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

class PneumaticFrame1:
    def __init__(self, master, initial_name, top_name, color, sol, reg_pwr, reg_set, reg_get, PSI):
        self.frame = Frame(master, borderwidth=2, relief=SUNKEN, bg=color)
        self.frame.pack()
        self.master = master
        self.frame_name = StringVar()
        self.frame_name.set(initial_name)
        self.state = 0
        self.fontType = "Comic Sans"
        self.activeColor = 'SpringGreen4'
        self.frameColor = color

        self.pressure = IntVar()
        self.lock_flag = IntVar()
        self.pressure.set("")

        self.power = Button(self.frame, text="PWR", activebackground=self.activeColor, command=lambda: self.toggle_pwr())
        self.extend = Button(self.frame, text="EXTEND", bg=self.activeColor, activebackground=self.activeColor, state=DISABLED, command=lambda: self.solenoid_extend())
        self.retract = Button(self.frame, text="RETRACT", activebackground=self.activeColor, state=DISABLED, command=lambda: self.solenoid_retract())
        self.set_label = Button(self.frame, text="SET LABEL", font=(self.fontType,7), command=lambda: self.get_label_input())
        self.observed_pressure = Entry(self.frame, width=5, state="readonly", textvariable = self.pressure)
        self.set_pressure_scale = Scale(self.frame, orient=HORIZONTAL, from_=0, to=92, resolution=0.5, bg=color, label="Set Pressure (PSI)", highlightthickness=0, command= self.set_pressure)
        self.custom_label = Label(self.frame, textvariable=self.frame_name, font=(self.fontType, 14), bg=color)
        self.label = Label(self.frame, text=initial_name, bg=color)
        self.lock = Checkbutton(self.frame, text="LOCK", bg=color, variable = self.lock_flag, command= self.lock)

        #Init the pressure scale to the default value
        self.set_pressure_scale.set(PSI)
        self.frame_name.set(top_name)

        self.frame.rowconfigure(0, minsize=30)
        self.custom_label.grid(row=0, column=0, columnspan=2, sticky=S)
        self.set_label.grid(column=0, row=1, columnspan=2)
        self.frame.rowconfigure(2, minsize=50)
        self.power.grid(column=0, row=2)
        self.observed_pressure.grid(column=1, row=2)
        self.set_pressure_scale.grid(column=0, row=3, columnspan=2, padx=20)
        self.frame.rowconfigure(4, minsize=50)
        self.extend.grid(column=0, row=4)
        self.retract.grid(column=1, row=4)
        self.label.grid(column=0, row=5)
        self.lock.grid(column=1, row=5)

        # Connect to Phidget Solid State Relay for solinoid control
        self.solenoid_switch = DigitalOutput()
        self.solenoid_switch.setDeviceSerialNumber(sol[0])
        self.solenoid_switch.setIsHubPortDevice(False)
        self.solenoid_switch.setHubPort(sol[1])
        self.solenoid_switch.setChannel(sol[2])
        self.solenoid_switch.openWaitForAttachment(5000)

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

        #One of the VINT Hubs on the SBC is used and needs special configuration
        if reg_get[0] == SBCH:
            self.pressure_reading.setIsHubPortDevice(True)
            self.pressure_reading.setHubPort(0)

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
            remember_state = self.set_pressure_scale.get()
            messagebox.showinfo(self.frame_name.get()+" Warning",
                                "Pressure will be set to zero. Acknowledge that " +self.frame_name.get()+" is in a safe configuration")
            # Change pressure to zero
            self.set_pressure_scale.set(0)
            self.set_pressure(0)
            time.sleep(0.5)
            self.frame.update()
            self.reg_switch.setState(False)
            time.sleep(0.5)
            self.set_pressure_scale.set(remember_state)

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
        self.solenoid_switch.setState(True)

    def solenoid_extend(self):
        self.retract.config(bg="SystemButtonFace")
        self.extend.config(bg=self.activeColor)
        self.solenoid_switch.setState(False)

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
        # Calculate volts/PSI, the maximum control voltage the regulator will accept is 5V
        ratio = 5 / range
        self.pressure_ctrl.setVoltage(float(val) * ratio)

    def update_pressure(self):
        if self.reg_switch.getState():
            try:
                val = float(self.pressure_reading.getSensorValue())
                PSI = val * 165.63 - 30.855
                PSI = round(PSI,2)
                self.pressure.set(PSI)
                # Low pressure check
                if PSI < (self.set_pressure_scale.get() - 3):
                    if self.frame.cget('bg') == "Red":
                        self.frame.config(bg=self.frameColor)
                        self.set_pressure_scale.config(bg=self.frameColor)
                        self.custom_label.config(bg=self.frameColor)
                        self.label.config(bg=self.frameColor)
                        self.lock.config(bg=self.frameColor)
                    else:
                        self.frame.config(bg='Red')
                        self.set_pressure_scale.config(bg="Red")
                        self.custom_label.config(bg="Red")
                        self.label.config(bg="Red")
                        self.lock.config(bg="Red")
                if PSI > (self.set_pressure_scale.get() - 3):
                    if self.frame.cget('bg') == "Red":
                        self.frame.config(bg=self.frameColor)
                        self.set_pressure_scale.config(bg=self.frameColor)
                        self.custom_label.config(bg=self.frameColor)
                        self.label.config(bg=self.frameColor)
                        self.lock.config(bg=self.frameColor)

            except:
                print("Init Air Pressure")
            root.after(200, self.update_pressure)
        else:
            self.pressure.set("")
    def lock(self):
        if self.lock_flag.get() == True:
            self.extend.config(state="disabled")
            self.retract.config(state="disabled")
            self.set_pressure_scale.config(state="disabled")
            self.power.config(state="disable")
        elif self.lock_flag.get() == False:
            self.extend.config(state="normal")
            self.retract.config(state="normal")
            self.set_pressure_scale.config(state="normal")
            self.power.config(state="normal")
class PneumaticFrame2:
    def __init__(self, master, initial_name, top_name, color, sol, reg_pwr, reg_set, reg_get, PSI):
        self.frame = Frame(master, borderwidth=2, relief=SUNKEN, bg=color)
        self.frame.pack()
        self.master = master
        self.frame_name = StringVar()
        self.frame_name.set(initial_name)
        self.state = 0
        self.fontType = "Comic Sans"
        self.activeColor = 'SpringGreen4'
        self.frameColor = color

        self.pressure = IntVar()
        self.lock_flag = IntVar()
        self.pressure.set("")

        self.power = Button(self.frame, text="PWR", activebackground=self.activeColor, command=lambda: self.toggle_pwr())
        self.set_label = Button(self.frame, text="SET LABEL", font=(self.fontType,7), command=lambda: self.get_label_input())
        self.observed_pressure = Entry(self.frame, width=5, state="readonly", textvariable = self.pressure)
        if self.frame_name.get() == "Hydro":
            self.set_pressure_scale = Scale(self.frame, orient=HORIZONTAL, from_=0, to=92, resolution=0.5, bg=color,
                                            label="Set Pressure (PSI)", highlightthickness=0, command=self.set_pressure)
        else:
            self.set_pressure_scale = Scale(self.frame, orient=HORIZONTAL, from_=0, to=50, resolution=0.5, bg=color,
                                            label="Set Pressure (PSI)", highlightthickness=0, command=self.set_pressure)
        self.custom_label = Label(self.frame, textvariable=self.frame_name, font=(self.fontType, 14), bg=color)
        self.label = Label(self.frame, text=initial_name, bg=color)
        self.lock = Checkbutton(self.frame, text="LOCK", bg=color, variable=self.lock_flag, command=self.lock)
        self.frame_name.set(top_name)

        # Init the pressure scale to the default value.
        self.set_pressure_scale.set(PSI)
        # Lock hydo at startup
        if initial_name == "Hydro":
            self.lock.select()
            self.set_pressure_scale.config(state="disabled")
            self.power.config(state="disable")

        self.frame.rowconfigure(0, minsize=30)
        self.custom_label.grid(row=0, column=0, columnspan=2, sticky=S)
        self.set_label.grid(column=0, row=1, columnspan=2)
        self.frame.rowconfigure(2, minsize=50)
        self.power.grid(column=0, row=2)
        self.observed_pressure.grid(column=1, row=2)
        self.set_pressure_scale.grid(column=0, row=3, columnspan=2, padx=20)
        self.frame.rowconfigure(4, minsize=5)
        self.label.grid(column=0, row=5)
        self.lock.grid(column=1, row=5)

        # Connect to Phidget Solid State Relay for solinoid control
        if self.frame_name.get() == "Hydro":
            self.solenoid_switch = DigitalOutput()
            self.solenoid_switch.setDeviceSerialNumber(sol[0])
            self.solenoid_switch.setIsHubPortDevice(False)
            self.solenoid_switch.setHubPort(sol[1])
            self.solenoid_switch.setChannel(sol[2])
            self.solenoid_switch.openWaitForAttachment(5000)

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

        #One of the VINT Hubs on the SBC is used and needs special configuration
        if reg_get[0] == SBCH:
            self.pressure_reading.setIsHubPortDevice(True)
            self.pressure_reading.setHubPort(0)

        self.pressure_reading.setChannel(reg_get[1])
        self.pressure_reading.openWaitForAttachment(5000)

    def toggle_pwr(self):
        #Turn on air channel
        if self.state == 0:
            #Turn on power to regulator and show active button color
            self.power.config(bg=self.activeColor)
            self.reg_switch.setState(True)
            if self.frame_name.get() == "Hydro":
                self.solenoid_switch.setState(True)

            #Start monitoring air pressure
            self.update_pressure()

            #Change state of air channel
            self.state = 1

        #Turn off air channel
        elif self.state == 1:
            remember_state = self.set_pressure_scale.get()
            if self.frame_name.get() != "Hydro":
                messagebox.showinfo(self.frame_name.get() + " Warning",
                                    "Pressure will be set to zero. Acknowledge that " + self.frame_name.get() + " is in a safe configuration")

            # Change pressure to zero
            self.set_pressure_scale.set(0)
            self.set_pressure(0)
            time.sleep(0.5)
            self.frame.update()
            self.reg_switch.setState(False)
            time.sleep(0.5)
            self.set_pressure_scale.set(remember_state)
            if self.frame_name.get() == "Hydro":
                self.solenoid_switch.setState(False)
                self.lock.select()
                self.set_pressure_scale.config(state="disabled")
                self.power.config(state="disable")

            #Turn off power to reguluator and remove active button color
            self.power.config(bg="SystemButtonFace")

            #Update air channel state
            self.state = 0

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
                PSI = val * 165.63 - 30.855
                PSI = round(PSI, 2)
                self.pressure.set(PSI)
                #Low pressure check
                if PSI < (self.set_pressure_scale.get() - 3):
                    if self.frame.cget('bg') == "Red":
                        self.frame.config(bg=self.frameColor)
                        self.set_pressure_scale.config(bg=self.frameColor)
                        self.custom_label.config(bg=self.frameColor)
                        self.label.config(bg=self.frameColor)
                        self.lock.config(bg=self.frameColor)
                    else:
                        self.frame.config(bg = 'Red')
                        self.set_pressure_scale.config(bg = "Red")
                        self.custom_label.config(bg = "Red")
                        self.label.config(bg="Red")
                        self.lock.config(bg="Red")
                if PSI > (self.set_pressure_scale.get() - 3):
                    if self.frame.cget('bg') == "Red":
                        self.frame.config(bg=self.frameColor)
                        self.set_pressure_scale.config(bg=self.frameColor)
                        self.custom_label.config(bg=self.frameColor)
                        self.label.config(bg=self.frameColor)
                        self.lock.config(bg=self.frameColor)
            except:
                print("Init Air Pressure")
            root.after(200, self.update_pressure)
        else:
            self.pressure.set("")

    def lock(self):
        if self.lock_flag.get() == True:
            self.set_pressure_scale.config(state="disabled")
            self.power.config(state="disable")
        elif self.lock_flag.get() == False:
            self.set_pressure_scale.config(state="normal")
            self.power.config(state="normal")

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

        frame1.grid(row=0, column=0)
        frame2.grid(row=0, column=1)
        frame3.grid(row=0, column=2)
        frame4.grid(row=1, column=0)
        frame5.grid(row=1, column=1)
        frame6.grid(row=1, column=2)
        frame7.grid(row=2, column=0, pady=25)
        frame8.grid(row=2, column=1)
        frame9.grid(row=2, column=2)

        out1 = PneumaticFrame1(frame1, "Channel #1", "LEFT LEG", colorArray[0], CH1_S, CH1_RP, CH1_RSP, CH1_ROP, 95)
        out2 = PneumaticFrame1(frame2, "Channel #2", "RIGHT LEG", colorArray[1], CH2_S, CH2_RP, CH2_RSP, CH2_ROP, 95)
        out3 = PneumaticFrame1(frame3, "Channel #3", "MANTIS GRIP", colorArray[2], CH3_S, CH3_RP, CH3_RSP, CH3_ROP, 95)
        out4 = PneumaticFrame1(frame4, "Channel #4", "VARD", colorArray[3], CH4_S, CH4_RP, CH4_RSP, CH4_ROP, 60)
        out5 = PneumaticFrame1(frame5, "Channel #5", "VARD GRIP", colorArray[4], CH5_S, CH5_RP, CH5_RSP, CH5_ROP, 95)
        out6 = PneumaticFrame1(frame6, "Channel #6", "Channel #6", colorArray[5], CH6_S, CH6_RP, CH6_RSP, CH6_ROP, 0)
        out7 = PneumaticFrame2(frame7, "Purge #1", "Standard Purge", 'DarkOliveGreen3', 0, PG1_RP, PG1_RSP, PG1_ROP, 25)
        out8 = PneumaticFrame2(frame8, "Purge #2", "Wrist Purge", 'DarkOliveGreen2', 0, PG2_RP, PG2_RSP, PG2_ROP, 25)
        out9 = PneumaticFrame2(frame9, "Hydro", "Hydro", 'DarkOrange2', HYD_RP, HYD_S, HYD_RSP, HYD_ROP, 95)

root = Tk()
TIMC = MainWindow(root, SetupMainWindow())
root.mainloop()
