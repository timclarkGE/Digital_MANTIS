###################################################################
# Tooling Inspection Motion Controller - Digital MANTIS Electrical
#
# Author: Timothy Clark
# Email: timothy.clark@ge.com
# Date: 03/13/2020
# Code Revision: 1
#
# Description:
#   This code runs the Digital MANTIS system which is composed of
# multiple motor axes. This also runs the RJ Camera system. There are
# six bulkhead connectors: camera, PTL, MANTIS Base, VARD, Mast, Wrist
#
# Revision 1 Update:
#   The code was modified to add keyboard binding so a user could use the keyboard instead of a mouse
#   Additionally, a Logitech F310 Gamepad can be connected to the Digital MANTIS Laptop and using 3rd party
#   Logitech software, one can map gamepad buttons to ascii characters allowing for control via the gamepad
#

from tkinter import *
from Phidget22.Devices.DCMotor import *
from Phidget22.Devices.CurrentInput import *
from Phidget22.Devices.DigitalOutput import *
from Phidget22.Devices.VoltageOutput import *
from Phidget22.Net import *

rainbow = ['SteelBlue1', 'DarkGoldenrod1', 'PaleGreen3','LightBlue3','DarkSlateGray3', 'MistyRose3','LightYellow3', 'dark khaki', 'LightSalmon2', 'chocolate1']
blue_checkers = ['LightSkyBlue1', 'LightSkyBlue3','LightSkyBlue1', 'LightSkyBlue3','LightSkyBlue1', 'LightSkyBlue3','LightSkyBlue1', 'LightSkyBlue3','LightSkyBlue1', 'LightSkyBlue3']
green_checkers = ['DarkOliveGreen1', 'DarkOliveGreen4','DarkOliveGreen1', 'DarkOliveGreen4','DarkOliveGreen1', 'DarkOliveGreen4','DarkOliveGreen1', 'DarkOliveGreen4','DarkOliveGreen1', 'DarkOliveGreen4']
green_checkers2 = ['DarkOliveGreen3', 'DarkOliveGreen4','DarkOliveGreen3', 'DarkOliveGreen4','DarkOliveGreen3', 'DarkOliveGreen4','DarkOliveGreen3', 'DarkOliveGreen4','DarkOliveGreen3', 'DarkOliveGreen4']
gold_checkers = ['gold2', 'gold3','gold2', 'gold3','gold2', 'gold3','gold2', 'gold3','gold2', 'gold3',]
orange_checkers = ['DarkOrange2', 'DarkOrange4','DarkOrange2', 'DarkOrange4','DarkOrange2', 'DarkOrange4','DarkOrange2', 'DarkOrange4','DarkOrange2', 'DarkOrange4',]

#Line required to look for Phidget devices on the network
Net.enableServerDiscovery(PhidgetServerType.PHIDGETSERVER_DEVICEREMOTE)

#System A SN:040
#SN = "040"
#HUB1 = 539552
#HUB2 = 539066

#System B
SN = "041"
HUB1 = 539079
HUB2 = 539520

#System C
#SN = "042"
#HUB1 = 539081
#HUB2 = 538800

#Current Multiplier
MULT = 1

class SetupMainWindow:
    def __init__(self):
        self.gui_width = 1050
        self.gui_height = 440

class MainWindow:
    def __init__(self, master, parameters):
        self.parameters = parameters
        self.master = master
        self.master.geometry(str(parameters.gui_width) + "x" + str(parameters.gui_height))
        self.master.title("R1 - TIMC Digital MANTIS Electrical - S/N: "+ SN)

        #Create Frame for Pnematics Control
        self.out0 = ControlFrame(master, blue_checkers)

        #Base Key Tool Movements
        master.bind('<KeyPress-w>', lambda event: self.out0.out2.jog("+"))
        master.bind('<KeyRelease-w>', lambda event: self.out0.out2.jog("0"))
        master.bind('<KeyPress-s>', lambda event: self.out0.out2.jog("-"))
        master.bind('<KeyRelease-s>', lambda event: self.out0.out2.jog("0"))
        master.bind('<KeyPress-d>', lambda event: self.out0.out1.jog("+"))
        master.bind('<KeyRelease-d>', lambda event: self.out0.out1.jog("0"))
        master.bind('<KeyPress-a>', lambda event: self.out0.out1.jog("-"))
        master.bind('<KeyRelease-a>', lambda event: self.out0.out1.jog("0"))

        #Vard Key Tool Movements
        master.bind('<KeyPress-5>', lambda event: self.out0.out4.jog("+"))
        master.bind('<KeyRelease-5>', lambda event: self.out0.out4.jog("0"))
        master.bind('<KeyPress-2>', lambda event: self.out0.out4.jog("-"))
        master.bind('<KeyRelease-2>', lambda event: self.out0.out4.jog("0"))
        master.bind('<KeyPress-3>', lambda event: self.out0.out3.jog("+"))
        master.bind('<KeyRelease-3>', lambda event: self.out0.out3.jog("0"))
        master.bind('<KeyPress-1>', lambda event: self.out0.out3.jog("-"))
        master.bind('<KeyRelease-1>', lambda event: self.out0.out3.jog("0"))

        #Camera Movement
        master.bind('<KeyPress-Left>', lambda event: self.out0.pan_move("L"))
        master.bind('<KeyRelease-Left>', lambda event: self.out0.pan_move("0"))
        master.bind('<KeyPress-Right>', lambda event: self.out0.pan_move("R"))
        master.bind('<KeyRelease-Right>', lambda event: self.out0.pan_move("0"))
        master.bind('<KeyPress-Up>', lambda event: self.out0.tilt_move("-"))
        master.bind('<KeyRelease-Up>', lambda event: self.out0.tilt_move("0"))
        master.bind('<KeyPress-Down>', lambda event: self.out0.tilt_move("+"))
        master.bind('<KeyRelease-Down>', lambda event: self.out0.tilt_move("0"))

        master.bind('<KeyPress-plus>', lambda event: self.out0.zoom("+"))
        master.bind('<KeyRelease-plus>', lambda event: self.out0.zoom("0"))
        master.bind('<KeyPress-minus>', lambda event: self.out0.zoom("-"))
        master.bind('<KeyRelease-minus>', lambda event: self.out0.zoom("0"))

        master.bind('<KeyPress-Insert>', lambda event: self.out0.focus("+"))
        master.bind('<KeyRelease-Insert>', lambda event: self.out0.focus("0"))
        master.bind('<KeyPress-Delete>', lambda event: self.out0.focus("-"))
        master.bind('<KeyRelease-Delete>', lambda event: self.out0.focus("0"))

        #Mast Movements
        master.bind('<KeyPress-Prior>', lambda event: self.out0.out5.jog("+"))
        master.bind('<KeyRelease-Prior>', lambda event: self.out0.out5.jog("0"))
        master.bind('<KeyPress-Next>', lambda event: self.out0.out5.jog("-"))
        master.bind('<KeyRelease-Next>', lambda event: self.out0.out5.jog("0"))
        master.bind('<KeyPress-i>', lambda event: self.out0.out7.jog("+"))
        master.bind('<KeyRelease-i>', lambda event: self.out0.out7.jog("0"))
        master.bind('<KeyPress-k>', lambda event: self.out0.out7.jog("-"))
        master.bind('<KeyRelease-k>', lambda event: self.out0.out7.jog("0"))
        master.bind('<KeyPress-l>', lambda event: self.out0.out6.jog("+"))
        master.bind('<KeyRelease-l>', lambda event: self.out0.out6.jog("0"))
        master.bind('<KeyPress-j>', lambda event: self.out0.out6.jog("-"))
        master.bind('<KeyRelease-j>', lambda event: self.out0.out6.jog("0"))

class popupWindow(object):
    def __init__(self, master, current_limit, max_velocity, acceleration, invert):
        top = self.top = Toplevel(master)

        self.invert = BooleanVar()

        #Store the current settings to the local window variables
        self.current_limit = current_limit
        self.max_velocity = max_velocity
        self.acceleration = acceleration
        self.invert.set(invert)

        #Create the scales
        self.scale_current_limit = Scale(top, orient=HORIZONTAL, from_=2, to=current_limit*MULT, resolution=.1,
                           label="Current Limit (A)", length=200)
        self.scale_max_velocity = Scale(top, orient=HORIZONTAL, from_=0.01, to=1, resolution=.01,
                           label="Max Velocity (%)", length=200)
        self.scale_acceleration = Scale(top, orient=HORIZONTAL, from_=0.1, to=100, resolution=0.1,
                           label="Max Acceleration (dty/s^2)", length=200)
        self.ckbx_invert = Checkbutton(top, text="Invert Axis Direction", variable=self.invert)
        self.btn_apply = Button(top, text="APPLY", command=self.apply_data)

        #Init the window to the current settings
        self.scale_current_limit.set(current_limit)
        self.scale_max_velocity.set(max_velocity)
        self.scale_acceleration.set(acceleration)

        #Grid the widgets
        self.scale_current_limit.grid(row=0, column=0, stick=W)
        self.scale_max_velocity.grid(row=1, column=0, sticky=W)
        self.scale_acceleration.grid(row=2, column=0, sticky=W)
        self.ckbx_invert.grid(row=3, column=0)
        self.btn_apply.grid(row=4,column=0)

    def apply_data(self):
        self.current_limit = self.scale_current_limit.get()
        self.max_velocity = self.scale_max_velocity.get()
        self.acceleration = self.scale_acceleration.get()
        self.cleanup()

    def cleanup(self):
        self.top.destroy()

class AxisFrame:
    def __init__(self, master, initial_name, move_pos_text, move_neg_text, serial_number, port, color, amp, vel):
        frame = Frame(master, borderwidth=2, relief=SUNKEN, bg=color)
        frame.pack()
        self.master = master
        self.frame_name = StringVar()
        self.frame_name.set(initial_name)
        self.fontType = "Comic Sans"

        #Set the parameters for the axis
        self.current_limit = amp          #2 to 25A
        self.max_velocity = vel           #0 to 1
        self.acceleration = 1         #0.1 to 100
        self.invert = FALSE             #TRUE or FALSE
        self.axis_name = initial_name
        self.move_pos_text  = move_pos_text
        self.move_neg_text = move_neg_text
        self.current_text = StringVar()

        self.jog_pos_btn = Button(frame, text=self.move_pos_text)
        self.jog_neg_btn = Button(frame, text=self.move_neg_text)
        self.configure_btn = Button(frame, text="CONFIGURE", font=(self.fontType,6), command=lambda: self.configure())
        self.current = Entry(frame, width=5, state=DISABLED, textvariable=self.current_text)
        self.speed = Scale(frame, orient=HORIZONTAL, from_=0.01, to=1, resolution=.01, bg=color, label="      Axis Speed", highlightthickness=0)
        self.custom_label = Label(frame, textvariable=self.frame_name, font=(self.fontType, 14), bg=color)
        self.label = Label(frame, text=initial_name, bg=color)

        self.speed.set(0.25)
        frame.rowconfigure(0, minsize=30)
        self.custom_label.grid(row=0, column=0, columnspan=2, sticky=S)
        self.jog_pos_btn.grid(column=0, row=1, pady=10)
        self.jog_neg_btn.grid(column=0, row=2, pady=10)
        self.current.grid(column=0, row=3,pady=5)
        self.speed.grid(column=0, row=4, padx=20)
        self.configure_btn.grid(column=0, row=5, pady=5)
        self.label.grid(column=0, row=6)

        #Connect to Phidget Motor Driver
        self.axis = DCMotor()
        self.axis.setDeviceSerialNumber(serial_number)
        self.axis.setIsHubPortDevice(False)
        self.axis.setHubPort(port)
        self.axis.setChannel(0)
        self.axis.openWaitForAttachment(5000)
        self.axis.setAcceleration(self.acceleration)

        self.axis_current = CurrentInput()
        self.axis_current.setDeviceSerialNumber(serial_number)
        self.axis_current.setIsHubPortDevice(False)
        self.axis_current.setHubPort(port)
        self.axis_current.setChannel(0)
        self.axis_current.openWaitForAttachment(5000)
        self.axis_current.setDataInterval(200)
        self.axis_current.setCurrentChangeTrigger(0.0)
        self.update_current()

        #Bind user button press of jog button to movement method
        self.jog_pos_btn.bind('<ButtonPress-1>', lambda event: self.jog("+"))
        self.jog_pos_btn.bind('<ButtonRelease-1>', lambda event: self.jog("0"))
        self.jog_neg_btn.bind('<ButtonPress-1>', lambda event: self.jog("-"))
        self.jog_neg_btn.bind('<ButtonRelease-1>', lambda event: self.jog("0"))

    def jog(self, direction):
        #Calculate the speed as a percentage of the maximum velocity
        velocity = float(self.speed.get())*self.max_velocity
        #Apply invert if necessary
        if self.invert == TRUE:
            velocity *= -1

        #Command Movement
        if direction == "+":
            self.axis.setTargetVelocity(velocity)
        elif direction == "-":
            self.axis.setTargetVelocity(-1*velocity)
        elif direction == "0":
            self.axis.setTargetVelocity(0)

    def update_current(self):
        self.current_text.set(abs(round(self.axis_current.getCurrent(),3)))
        root.after(200,self.update_current)

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

        #Update Phidget parameters
        self.axis.setCurrentLimit(self.current_limit)
        self.axis.setAcceleration(self.acceleration)

class ControlFrame:
    def __init__(self, master, colorArray):
        frame1 = Frame(master, borderwidth=2, relief=SUNKEN)
        frame2 = Frame(master, borderwidth=2, relief=SUNKEN)
        frame3 = Frame(master, borderwidth=2, relief=SUNKEN)
        frame4 = Frame(master, borderwidth=2, relief=SUNKEN)
        frame5 = Frame(master, borderwidth=2, relief=SUNKEN)
        frame6 = Frame(master, borderwidth=2, relief=SUNKEN)
        frame7 = Frame(master, borderwidth=2, relief=SUNKEN)
        camera_frame = Frame(master, borderwidth=2, relief=SUNKEN)

        frame1.grid(row=1,column=0)
        frame2.grid(row=1,column=1)
        frame3.grid(row=1, column=2)
        frame4.grid(row=1, column=3)
        frame5.grid(row=1, column=4)
        frame6.grid(row=1, column=5)
        frame7.grid(row=1, column=6)
        camera_frame.grid(row=3,column=0, columnspan=7, sticky=W)

        self.out1 = AxisFrame(frame1, "BASE CIRC", "VESSEL RIGHT", "VESSEL LEFT", HUB1, 5, colorArray[0], 3.3, 0.55)
        self.out2 = AxisFrame(frame2, "BASE AUX", "CW/IN", "CCW/OUT", HUB2, 0, colorArray[1], 2.2, 0.11)
        self.out3 = AxisFrame(frame3, "VARD ROT", "CW", "CCW", HUB1, 3, colorArray[2], 2.2, 0.15)
        self.out4 = AxisFrame(frame4, "VARD VERT", "UP", "DOWN", HUB1, 4, colorArray[3], 7.8, 0.54)
        self.out5 = AxisFrame(frame5, "DA MAST", "UP", "DOWN", HUB1, 0, colorArray[4], 8, 0.86)
        self.out6 = AxisFrame(frame6, "DA PAN", "CW", "CCW", HUB1, 2, colorArray[5], 3.0, 0.30)
        self.out7 = AxisFrame(frame7, "DA TILT", "UP", "DOWN", HUB1, 1, colorArray[6], 3.6, 0.57)

        #RJ Camera Control Code
        self.invert_tilt = BooleanVar()
        self.invert_pan = BooleanVar()
        self.btn_power = Button(camera_frame, text="PWR", font="Courier, 12", command=self.toggle_power)
        self.btn_near = Button(camera_frame, text="NEAR", font="Courier, 12", width=7)
        self.btn_far = Button(camera_frame, text="FAR", font="Courier, 12", width=7)
        self.btn_wide = Button(camera_frame, text="WIDE", font="Courier, 12", width=7)
        self.btn_tele = Button(camera_frame, text="TELE", font="Courier, 12", width=7)
        self.btn_ms = Button(camera_frame, text="MS", font="Courier, 12", width=7)
        self.left_light_scale = Scale(camera_frame, orient=VERTICAL, from_=0, to=0.45, resolution=0.01, command=self.update_left_intensity)
        self.right_light_scale = Scale(camera_frame, orient=VERTICAL, from_=0, to=0.45, resolution=0.01, command=self.update_right_intensity)
        self.label_lights = Label(camera_frame, text="  Light Intensity")
        self.btn_tilt_up = Button(camera_frame, text="TILT UP", font="Courier, 12", width=10)
        self.btn_tilt_down = Button(camera_frame, text="TILT DOWN", font="Courier, 12", width=10)
        self.btn_pan_right = Button(camera_frame, text="PAN RIGHT", font="Courier, 12", width=10)
        self.btn_pan_left = Button(camera_frame, text="PAN LEFT", font="Courier, 12", width=10)
        self.tilt_speed = Scale(camera_frame, orient=HORIZONTAL, from_=0.01, to=.5, resolution=0.01)
        self.pan_speed = Scale(camera_frame, orient=HORIZONTAL, from_=0.01, to=.5, resolution=0.01)
        self.ckbx_invert_tilt = Checkbutton(camera_frame, text="Invert Tilt", variable=self.invert_tilt)
        self.ckbx_invert_pan = Checkbutton(camera_frame, text="Invert Pan", variable=self.invert_pan)
        self.activeColor = 'SpringGreen4'

        self.tilt_speed.set(0.15)
        self.pan_speed.set(0.15)

        self.btn_power.grid(row=0, column=0, padx=60)
        self.btn_ms.grid(row=1, column=0, padx=5, pady=5)
        self.btn_near.grid(row=0, column=2, padx=20, pady=10)
        self.btn_far.grid(row=1, column=2, padx=20, pady=10)
        self.btn_tele.grid(row=0, column=3, padx=20, pady=10)
        self.btn_wide.grid(row=1, column=3, padx=20, pady=10)
        self.left_light_scale.grid(row=0, column=4, rowspan=3, padx=20, pady=5)
        self.right_light_scale.grid(row=0, column=5, rowspan=3, padx=45, pady=5)
        self.label_lights.grid(row=3, column=4, columnspan=2, padx=45, sticky=N)
        self.btn_tilt_up.grid(row=0, column=6, padx=20, pady=5)
        self.btn_tilt_down.grid(row=1, column=6, padx=20, pady=5)
        self.btn_pan_right.grid(row=0, column=8, padx=20, pady=5, rowspan=2)
        self.btn_pan_left.grid(row=0, column=7, padx=20, pady=5, rowspan=2)
        self.tilt_speed.grid(row=2, column=6)
        self.pan_speed.grid(row=2, column=7, columnspan=2)
        self.ckbx_invert_tilt.grid(row=3,column=6)
        self.ckbx_invert_pan.grid(row=3, column=7, columnspan=2)

        #Connect to Phidget Devices
        self.power = DigitalOutput()
        self.power.setDeviceSerialNumber(HUB2)
        self.power.setIsHubPortDevice(False)
        self.power.setHubPort(1)
        self.power.setChannel(0)
        self.power.openWaitForAttachment(5000)

        self.manual_select = DigitalOutput()
        self.manual_select.setDeviceSerialNumber(HUB2)
        self.manual_select.setIsHubPortDevice(False)
        self.manual_select.setHubPort(1)
        self.manual_select.setChannel(1)
        self.manual_select.openWaitForAttachment(5000)

        self.near = DigitalOutput()
        self.near.setDeviceSerialNumber(HUB2)
        self.near.setIsHubPortDevice(False)
        self.near.setHubPort(1)
        self.near.setChannel(2)
        self.near.openWaitForAttachment(5000)

        self.far = DigitalOutput()
        self.far.setDeviceSerialNumber(HUB2)
        self.far.setIsHubPortDevice(False)
        self.far.setHubPort(1)
        self.far.setChannel(3)
        self.far.openWaitForAttachment(5000)

        self.wide = DigitalOutput()
        self.wide.setDeviceSerialNumber(HUB2)
        self.wide.setIsHubPortDevice(False)
        self.wide.setHubPort(1)
        self.wide.setChannel(4)
        self.wide.openWaitForAttachment(5000)

        self.tele = DigitalOutput()
        self.tele.setDeviceSerialNumber(HUB2)
        self.tele.setIsHubPortDevice(False)
        self.tele.setHubPort(1)
        self.tele.setChannel(5)
        self.tele.openWaitForAttachment(5000)

        self.left_light = VoltageOutput()
        self.left_light.setDeviceSerialNumber(HUB2)
        self.left_light.setIsHubPortDevice(False)
        self.left_light.setHubPort(2)
        self.left_light.setChannel(0)
        self.left_light.openWaitForAttachment(5000)

        self.right_light = VoltageOutput()
        self.right_light.setDeviceSerialNumber(HUB2)
        self.right_light.setIsHubPortDevice(False)
        self.right_light.setHubPort(3)
        self.right_light.setChannel(0)
        self.right_light.openWaitForAttachment(5000)

        self.pan = VoltageOutput()
        self.pan.setDeviceSerialNumber(HUB2)
        self.pan.setIsHubPortDevice(False)
        self.pan.setHubPort(5)
        self.pan.setChannel(0)
        self.pan.openWaitForAttachment(5000)

        self.tilt = VoltageOutput()
        self.tilt.setDeviceSerialNumber(HUB2)
        self.tilt.setIsHubPortDevice(False)
        self.tilt.setHubPort(4)
        self.tilt.setChannel(0)
        self.tilt.openWaitForAttachment(5000)

        self.btn_near.bind('<ButtonPress-1>', lambda event: self.focus("+"))
        self.btn_near.bind('<ButtonRelease-1>', lambda event: self.focus("0"))
        self.btn_far.bind('<ButtonPress-1>', lambda event: self.focus("-"))
        self.btn_far.bind('<ButtonRelease-1>', lambda event: self.focus("0"))
        self.btn_wide.bind('<ButtonPress-1>', lambda event: self.zoom("-"))
        self.btn_wide.bind('<ButtonRelease-1>', lambda event: self.zoom("0"))
        self.btn_tele.bind('<ButtonPress-1>', lambda event: self.zoom("+"))
        self.btn_tele.bind('<ButtonRelease-1>', lambda event: self.zoom("0"))
        self.btn_ms.bind('<ButtonPress-1>', lambda event: self.focus_type("ON"))
        self.btn_ms.bind('<ButtonRelease-1>', lambda event: self.focus_type("OFF"))

        self.btn_tilt_up.bind('<ButtonPress-1>', lambda event: self.tilt_move("-"))
        self.btn_tilt_up.bind('<ButtonRelease-1>', lambda event: self.tilt_move("0"))
        self.btn_tilt_down.bind('<ButtonPress-1>', lambda event: self.tilt_move("+"))
        self.btn_tilt_down.bind('<ButtonRelease-1>', lambda event: self.tilt_move("0"))
        self.btn_pan_right.bind('<ButtonPress-1>', lambda event: self.pan_move("R"))
        self.btn_pan_right.bind('<ButtonRelease-1>', lambda event: self.pan_move("0"))
        self.btn_pan_left.bind('<ButtonPress-1>', lambda event: self.pan_move("L"))
        self.btn_pan_left.bind('<ButtonRelease-1>', lambda event: self.pan_move("0"))

    def toggle_power(self):
        if self.power.getState() == True:
            self.power.setState(False)
            self.btn_power.config(bg="SystemButtonFace")
        elif self.power.getState() == False:
            self.power.setState(True)
            self.btn_power.config(bg=self.activeColor)

    def update_left_intensity(self, val):
        self.left_light.setVoltage(float(val))

    def update_right_intensity(self, val):
        self.right_light.setVoltage(float(val))

    def focus(self, direction):
        if direction == "+":
            self.near.setState(TRUE)
        elif direction == "-":
            self.far.setState(TRUE)
        elif direction == "0":
            self.far.setState(FALSE)
            self.near.setState(FALSE)

    def zoom(self, direction):
        if direction == "+":
            self.tele.setState(TRUE)
        elif direction == "-":
            self.wide.setState(TRUE)
        elif direction == "0":
            self.tele.setState(FALSE)
            self.wide.setState(FALSE)

    def pan_move(self, direction):
        voltage = float(self.pan_speed.get())
        if self.invert_pan.get():
            voltage *= -1
        if direction == "R":
            self.pan.setVoltage(voltage)
        elif direction == "L":
            self.pan.setVoltage(-1*voltage)
        elif direction == "0":
            self.pan.setVoltage(0)

    def tilt_move(self, direction):
        voltage = float(self.tilt_speed.get())
        if self.invert_tilt.get():
            voltage *= -1
        if direction == "+":
            self.tilt.setVoltage(voltage)
        elif direction == "-":
            self.tilt.setVoltage(-1*voltage)
        elif direction == "0":
            self.tilt.setVoltage(0)

    def focus_type(self, state):
        if state == "ON":
            self.manual_select.setState(True)
        elif state == "OFF":
            self.manual_select.setState(False)

root = Tk()
TIMC = MainWindow(root, SetupMainWindow())
root.mainloop()
