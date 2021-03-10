###################################################################
# Tooling Inspection Motion Controller - Digital MANTIS Electrical
#
# Author: Timothy Clark
# Email: timothy.clark@ge.com
# Date: 03/09/2021
# Code Revision: 2A BETA
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
# Revision 2A BETA Update:
#   There has been a request to update the code to accept additional hardware to run a second RJ overview camera. The
#   enclosure would need the following extra components:
#       (4) Voltage Output, P/N: OUT1001_0
#       (4) Centent Linear Amplifiers, P/N: CN0121A
#       (?) Various terminal blocks, resistors, relay terminal block
#       (1) Camera bulkhead connector
#       (2) BNC bulkhead connectors
#
#   I also created offline mode so I could view the GUI without the cabinet hooked up.


from tkinter import *
from Phidget22.Devices.DCMotor import *
from Phidget22.Devices.CurrentInput import *
from Phidget22.Devices.DigitalOutput import *
from Phidget22.Devices.VoltageOutput import *
from Phidget22.Net import *

rainbow = ['SteelBlue1', 'DarkGoldenrod1', 'PaleGreen3', 'LightBlue3', 'DarkSlateGray3', 'MistyRose3', 'LightYellow3',
           'dark khaki', 'LightSalmon2', 'chocolate1']
blue_checkers = ['LightSkyBlue1', 'LightSkyBlue3', 'LightSkyBlue1', 'LightSkyBlue3', 'LightSkyBlue1', 'LightSkyBlue3',
                 'LightSkyBlue1', 'LightSkyBlue3', 'LightSkyBlue1', 'LightSkyBlue3']
green_checkers = ['DarkOliveGreen1', 'DarkOliveGreen4', 'DarkOliveGreen1', 'DarkOliveGreen4', 'DarkOliveGreen1',
                  'DarkOliveGreen4', 'DarkOliveGreen1', 'DarkOliveGreen4', 'DarkOliveGreen1', 'DarkOliveGreen4']
green_checkers2 = ['DarkOliveGreen3', 'DarkOliveGreen4', 'DarkOliveGreen3', 'DarkOliveGreen4', 'DarkOliveGreen3',
                   'DarkOliveGreen4', 'DarkOliveGreen3', 'DarkOliveGreen4', 'DarkOliveGreen3', 'DarkOliveGreen4']
gold_checkers = ['gold2', 'gold3', 'gold2', 'gold3', 'gold2', 'gold3', 'gold2', 'gold3', 'gold2', 'gold3', ]
orange_checkers = ['DarkOrange2', 'DarkOrange4', 'DarkOrange2', 'DarkOrange4', 'DarkOrange2', 'DarkOrange4',
                   'DarkOrange2', 'DarkOrange4', 'DarkOrange2', 'DarkOrange4', ]

# Line required to look for Phidget devices on the network
Net.enableServerDiscovery(PhidgetServerType.PHIDGETSERVER_DEVICEREMOTE)

# System A SN:040
# SN = "040"
# HUB1 = 539552
# HUB2 = 539066

# System B
# SN = "041"
# HUB1 = 539079
# HUB2 = 539520

# System C
SN = "042"
HUB1 = 539081
HUB2 = 538800

# Current Multiplier
MULT = 1


class SetupMainWindow:
    def __init__(self):
        self.gui_width = 1050
        self.gui_height = 608


class MainWindow:
    def __init__(self, master, parameters):
        self.parameters = parameters
        self.master = master
        self.master.geometry(str(parameters.gui_width) + "x" + str(parameters.gui_height))
        self.master.title("R2 BETA - TIMC Digital MANTIS Electrical - S/N: " + SN)

        # Create Frame for Pnematics Control
        self.out0 = ControlFrame(master, blue_checkers)

        # Base Key Tool Movements
        master.bind('<KeyPress-w>', lambda event: self.out0.out2.jog("+"))
        master.bind('<KeyRelease-w>', lambda event: self.out0.out2.jog("0"))
        master.bind('<KeyPress-s>', lambda event: self.out0.out2.jog("-"))
        master.bind('<KeyRelease-s>', lambda event: self.out0.out2.jog("0"))
        master.bind('<KeyPress-d>', lambda event: self.out0.out1.jog("+"))
        master.bind('<KeyRelease-d>', lambda event: self.out0.out1.jog("0"))
        master.bind('<KeyPress-a>', lambda event: self.out0.out1.jog("-"))
        master.bind('<KeyRelease-a>', lambda event: self.out0.out1.jog("0"))

        # Vard Key Tool Movements
        master.bind('<KeyPress-5>', lambda event: self.out0.out4.jog("+"))
        master.bind('<KeyRelease-5>', lambda event: self.out0.out4.jog("0"))
        master.bind('<KeyPress-2>', lambda event: self.out0.out4.jog("-"))
        master.bind('<KeyRelease-2>', lambda event: self.out0.out4.jog("0"))
        master.bind('<KeyPress-3>', lambda event: self.out0.out3.jog("+"))
        master.bind('<KeyRelease-3>', lambda event: self.out0.out3.jog("0"))
        master.bind('<KeyPress-1>', lambda event: self.out0.out3.jog("-"))
        master.bind('<KeyRelease-1>', lambda event: self.out0.out3.jog("0"))

        # Camera Movement
        master.bind('<KeyPress-Left>', lambda event: self.out0.pan_move_1("L"))
        master.bind('<KeyRelease-Left>', lambda event: self.out0.pan_move_1("0"))
        master.bind('<KeyPress-Right>', lambda event: self.out0.pan_move_1("R"))
        master.bind('<KeyRelease-Right>', lambda event: self.out0.pan_move_1("0"))
        master.bind('<KeyPress-Up>', lambda event: self.out0.tilt_move_1("-"))
        master.bind('<KeyRelease-Up>', lambda event: self.out0.tilt_move_1("0"))
        master.bind('<KeyPress-Down>', lambda event: self.out0.tilt_move_1("+"))
        master.bind('<KeyRelease-Down>', lambda event: self.out0.tilt_move_1("0"))

        master.bind('<KeyPress-plus>', lambda event: self.out0.zoom_1("+"))
        master.bind('<KeyRelease-plus>', lambda event: self.out0.zoom_1("0"))
        master.bind('<KeyPress-minus>', lambda event: self.out0.zoom_1("-"))
        master.bind('<KeyRelease-minus>', lambda event: self.out0.zoom_1("0"))

        master.bind('<KeyPress-Insert>', lambda event: self.out0.focus_1("+"))
        master.bind('<KeyRelease-Insert>', lambda event: self.out0.focus_1("0"))
        master.bind('<KeyPress-Delete>', lambda event: self.out0.focus_1("-"))
        master.bind('<KeyRelease-Delete>', lambda event: self.out0.focus_1("0"))

        # Mast Movements
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

        # Store the current settings to the local window variables
        self.current_limit = current_limit
        self.max_velocity = max_velocity
        self.acceleration = acceleration
        self.invert.set(invert)

        # Create the scales
        self.scale_current_limit = Scale(top, orient=HORIZONTAL, from_=2, to=current_limit * MULT, resolution=.1,
                                         label="Current Limit (A)", length=200)
        self.scale_max_velocity = Scale(top, orient=HORIZONTAL, from_=0.01, to=1, resolution=.01,
                                        label="Max Velocity (%)", length=200)
        self.scale_acceleration = Scale(top, orient=HORIZONTAL, from_=0.1, to=100, resolution=0.1,
                                        label="Max Acceleration (dty/s^2)", length=200)
        self.ckbx_invert = Checkbutton(top, text="Invert Axis Direction", variable=self.invert)
        self.btn_apply = Button(top, text="APPLY", command=self.apply_data)

        # Init the window to the current settings
        self.scale_current_limit.set(current_limit)
        self.scale_max_velocity.set(max_velocity)
        self.scale_acceleration.set(acceleration)

        # Grid the widgets
        self.scale_current_limit.grid(row=0, column=0, stick=W)
        self.scale_max_velocity.grid(row=1, column=0, sticky=W)
        self.scale_acceleration.grid(row=2, column=0, sticky=W)
        self.ckbx_invert.grid(row=3, column=0)
        self.btn_apply.grid(row=4, column=0)

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

        # Set the parameters for the axis
        self.current_limit = amp  # 2 to 25A
        self.max_velocity = vel  # 0 to 1
        self.acceleration = 1  # 0.1 to 100
        self.invert = FALSE  # TRUE or FALSE
        self.axis_name = initial_name
        self.move_pos_text = move_pos_text
        self.move_neg_text = move_neg_text
        self.current_text = StringVar()

        self.jog_pos_btn = Button(frame, text=self.move_pos_text)
        self.jog_neg_btn = Button(frame, text=self.move_neg_text)
        self.configure_btn = Button(frame, text="CONFIGURE", font=(self.fontType, 6), command=lambda: self.configure())
        self.current = Entry(frame, width=5, state=DISABLED, textvariable=self.current_text)
        self.speed = Scale(frame, orient=HORIZONTAL, from_=0.01, to=1, resolution=.01, bg=color,
                           label="      Axis Speed", highlightthickness=0)
        self.custom_label = Label(frame, textvariable=self.frame_name, font=(self.fontType, 14), bg=color)
        self.label = Label(frame, text=initial_name, bg=color)

        self.speed.set(0.25)
        frame.rowconfigure(0, minsize=30)
        self.custom_label.grid(row=0, column=0, columnspan=2, sticky=S)
        self.jog_pos_btn.grid(column=0, row=1, pady=10)
        self.jog_neg_btn.grid(column=0, row=2, pady=10)
        self.current.grid(column=0, row=3, pady=5)
        self.speed.grid(column=0, row=4, padx=20)
        self.configure_btn.grid(column=0, row=5, pady=5)
        self.label.grid(column=0, row=6)

        # Connect to Phidget Motor Driver
        self.axis = DCMotor()
        self.axis.setDeviceSerialNumber(serial_number)
        self.axis.setIsHubPortDevice(False)
        self.axis.setHubPort(port)
        self.axis.setChannel(0)
        try:
            self.axis.openWaitForAttachment(1000)
            self.axis.setAcceleration(self.acceleration)
        except PhidgetException as e:
            print("Failed to open (" + initial_name + "): " + e.details)

        self.axis_current = CurrentInput()
        self.axis_current.setDeviceSerialNumber(serial_number)
        self.axis_current.setIsHubPortDevice(False)
        self.axis_current.setHubPort(port)
        self.axis_current.setChannel(0)
        try:
            self.axis_current.openWaitForAttachment(1000)
            self.axis_current.setDataInterval(200)
            self.axis_current.setCurrentChangeTrigger(0.0)
            self.update_current()
        except PhidgetException as e:
            print("Failed to open (" + initial_name + "): " + e.details)

        # Bind user button press of jog button to movement method
        self.jog_pos_btn.bind('<ButtonPress-1>', lambda event: self.jog("+"))
        self.jog_pos_btn.bind('<ButtonRelease-1>', lambda event: self.jog("0"))
        self.jog_neg_btn.bind('<ButtonPress-1>', lambda event: self.jog("-"))
        self.jog_neg_btn.bind('<ButtonRelease-1>', lambda event: self.jog("0"))

    def jog(self, direction):
        # Calculate the speed as a percentage of the maximum velocity
        velocity = float(self.speed.get()) * self.max_velocity
        # Apply invert if necessary
        if self.invert == TRUE:
            velocity *= -1

        # Command Movement
        if direction == "+":
            self.axis.setTargetVelocity(velocity)
        elif direction == "-":
            self.axis.setTargetVelocity(-1 * velocity)
        elif direction == "0":
            self.axis.setTargetVelocity(0)

    def update_current(self):
        self.current_text.set(abs(round(self.axis_current.getCurrent(), 3)))
        root.after(200, self.update_current)

    def configure(self):
        # current_limit, max_velocity, acceleration, invert
        self.window = popupWindow(self.master, self.current_limit, self.max_velocity, self.acceleration, self.invert)
        self.configure_btn.config(state=DISABLED)
        self.master.wait_window(self.window.top)
        self.configure_btn.config(state=NORMAL)

        # Set the new parameters from the configuration window
        self.current_limit = self.window.current_limit
        self.max_velocity = self.window.max_velocity
        self.acceleration = self.window.acceleration
        self.invert = self.window.invert.get()

        # Update Phidget parameters
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
        camera_frame_1 = Frame(master, borderwidth=2, relief=SUNKEN, bg='LightSkyBlue2')
        camera_frame_2 = Frame(master, borderwidth=2, relief=SUNKEN, bg='light goldenrod yellow')

        frame1.grid(row=1, column=0)
        frame2.grid(row=1, column=1)
        frame3.grid(row=1, column=2)
        frame4.grid(row=1, column=3)
        frame5.grid(row=1, column=4)
        frame6.grid(row=1, column=5)
        frame7.grid(row=1, column=6)
        camera_frame_1.grid(row=3, column=0, columnspan=7, sticky=NSEW)
        camera_frame_2.grid(row=4, column=0, columnspan=7, sticky=NSEW)

        self.out1 = AxisFrame(frame1, "BASE CIRC", "VESSEL RIGHT", "VESSEL LEFT", HUB1, 5, colorArray[0], 3.3, 0.55)
        self.out2 = AxisFrame(frame2, "BASE AUX", "CW/IN", "CCW/OUT", HUB2, 0, colorArray[1], 2.2, 0.11)
        self.out3 = AxisFrame(frame3, "VARD ROT", "CW", "CCW", HUB1, 3, colorArray[2], 2.2, 0.15)
        self.out4 = AxisFrame(frame4, "VARD VERT", "UP", "DOWN", HUB1, 4, colorArray[3], 7.8, 0.54)
        self.out5 = AxisFrame(frame5, "DA MAST", "UP", "DOWN", HUB1, 0, colorArray[4], 8, 0.86)
        self.out6 = AxisFrame(frame6, "DA PAN", "CW", "CCW", HUB1, 2, colorArray[5], 3.0, 0.30)
        self.out7 = AxisFrame(frame7, "DA TILT", "UP", "DOWN", HUB1, 1, colorArray[6], 3.6, 0.57)

        # RJ Camera Control: Code Tool Camera
        self.invert_tilt_1 = BooleanVar()
        self.invert_pan_1 = BooleanVar()
        self.btn_power_1 = Button(camera_frame_1, text="PWR", font="Courier, 12", command=self.toggle_power_1)
        self.btn_near_1 = Button(camera_frame_1, text="NEAR", font="Courier, 12", width=7)
        self.btn_far_1 = Button(camera_frame_1, text="FAR", font="Courier, 12", width=7)
        self.btn_wide_1 = Button(camera_frame_1, text="WIDE", font="Courier, 12", width=7)
        self.btn_tele_1 = Button(camera_frame_1, text="TELE", font="Courier, 12", width=7)
        self.btn_ms_1 = Button(camera_frame_1, text="MS", font="Courier, 12", width=7)
        self.left_light_scale_1 = Scale(camera_frame_1, orient=VERTICAL, from_=0, to=0.45, resolution=0.01,
                                        command=self.update_left_intensity_1, bg='LightSkyBlue2', highlightthickness=0)
        self.right_light_scale_1 = Scale(camera_frame_1, orient=VERTICAL, from_=0, to=0.45, resolution=0.01,
                                         command=self.update_right_intensity_1, bg='LightSkyBlue2',
                                         highlightthickness=0)
        self.label_lights_1 = Label(camera_frame_1, text="  Light Intensity", bg='LightSkyBlue2')
        self.label_camera_type_1 = Label(camera_frame_1, text="TOOL CAMERA", font=("TkDefaultFont", 14),
                                         bg='LightSkyBlue2')
        self.btn_tilt_up_1 = Button(camera_frame_1, text="TILT UP", font="Courier, 12", width=10)
        self.btn_tilt_down_1 = Button(camera_frame_1, text="TILT DOWN", font="Courier, 12", width=10)
        self.btn_pan_right_1 = Button(camera_frame_1, text="PAN RIGHT", font="Courier, 12", width=10)
        self.btn_pan_left_1 = Button(camera_frame_1, text="PAN LEFT", font="Courier, 12", width=10)
        self.tilt_speed_1 = Scale(camera_frame_1, orient=HORIZONTAL, from_=0.01, to=.5, resolution=0.01,
                                  bg='LightSkyBlue2', highlightthickness=0)
        self.pan_speed_1 = Scale(camera_frame_1, orient=HORIZONTAL, from_=0.01, to=.5, resolution=0.01,
                                 bg='LightSkyBlue2', highlightthickness=0)
        self.ckbx_invert_tilt_1 = Checkbutton(camera_frame_1, text="Invert Tilt", variable=self.invert_tilt_1,
                                              bg='LightSkyBlue2')
        self.ckbx_invert_pan_1 = Checkbutton(camera_frame_1, text="Invert Pan", variable=self.invert_pan_1,
                                             bg='LightSkyBlue2')
        self.activeColor_1 = 'SpringGreen4'

        self.tilt_speed_1.set(0.15)
        self.pan_speed_1.set(0.15)

        # RJ Camera Control: Overview Camera
        self.invert_tilt_2 = BooleanVar()
        self.invert_pan_2 = BooleanVar()
        self.btn_power_2 = Button(camera_frame_2, text="PWR", font="Courier, 12", command=self.toggle_power_2)
        self.btn_near_2 = Button(camera_frame_2, text="NEAR", font="Courier, 12", width=7)
        self.btn_far_2 = Button(camera_frame_2, text="FAR", font="Courier, 12", width=7)
        self.btn_wide_2 = Button(camera_frame_2, text="WIDE", font="Courier, 12", width=7)
        self.btn_tele_2 = Button(camera_frame_2, text="TELE", font="Courier, 12", width=7)
        self.btn_ms_2 = Button(camera_frame_2, text="MS", font="Courier, 12", width=7)
        self.left_light_scale_2 = Scale(camera_frame_2, orient=VERTICAL, from_=0, to=0.45, resolution=0.01,
                                        command=self.update_left_intensity_2, bg='light goldenrod yellow',
                                        highlightthickness=0)
        self.right_light_scale_2 = Scale(camera_frame_2, orient=VERTICAL, from_=0, to=0.45, resolution=0.01,
                                         command=self.update_right_intensity_2, bg='light goldenrod yellow',
                                         highlightthickness=0)
        self.label_lights_2 = Label(camera_frame_2, text="  Light Intensity", bg='light goldenrod yellow')
        self.label_camera_type_2 = Label(camera_frame_2, text="OVERVIEW CAMERA", font=("TkDefaultFont", 14),
                                         bg='light goldenrod yellow')
        self.btn_tilt_up_2 = Button(camera_frame_2, text="TILT UP", font="Courier, 12", width=10)
        self.btn_tilt_down_2 = Button(camera_frame_2, text="TILT DOWN", font="Courier, 12", width=10)
        self.btn_pan_right_2 = Button(camera_frame_2, text="PAN RIGHT", font="Courier, 12", width=10)
        self.btn_pan_left_2 = Button(camera_frame_2, text="PAN LEFT", font="Courier, 12", width=10)
        self.tilt_speed_2 = Scale(camera_frame_2, orient=HORIZONTAL, from_=0.01, to=.5, resolution=0.01,
                                  bg='light goldenrod yellow', highlightthickness=0)
        self.pan_speed_2 = Scale(camera_frame_2, orient=HORIZONTAL, from_=0.01, to=.5, resolution=0.01,
                                 bg='light goldenrod yellow', highlightthickness=0)
        self.ckbx_invert_tilt_2 = Checkbutton(camera_frame_2, text="Invert Tilt", variable=self.invert_tilt_2,
                                              bg='light goldenrod yellow')
        self.ckbx_invert_pan_2 = Checkbutton(camera_frame_2, text="Invert Pan", variable=self.invert_pan_2,
                                             bg='light goldenrod yellow')
        self.activeColor_2 = 'SpringGreen4'

        self.tilt_speed_2.set(0.15)
        self.pan_speed_2.set(0.15)

        # Grid the Tool Camera Controls
        self.btn_power_1.grid(row=0, column=0, padx=60)
        self.btn_ms_1.grid(row=1, column=0, padx=5, pady=5)
        self.btn_near_1.grid(row=0, column=2, padx=20, pady=10)
        self.btn_far_1.grid(row=1, column=2, padx=20, pady=10)
        self.btn_tele_1.grid(row=0, column=3, padx=20, pady=10)
        self.btn_wide_1.grid(row=1, column=3, padx=20, pady=10)
        self.label_camera_type_1.grid(row=2, column=0, columnspan=4)
        self.left_light_scale_1.grid(row=0, column=4, rowspan=3, padx=20, pady=5)
        self.right_light_scale_1.grid(row=0, column=5, rowspan=3, padx=45, pady=5)
        self.label_lights_1.grid(row=3, column=4, columnspan=2, padx=45, sticky=N)
        self.btn_tilt_up_1.grid(row=0, column=6, padx=20, pady=5)
        self.btn_tilt_down_1.grid(row=1, column=6, padx=20, pady=5)
        self.btn_pan_right_1.grid(row=0, column=8, padx=20, pady=5, rowspan=2)
        self.btn_pan_left_1.grid(row=0, column=7, padx=20, pady=5, rowspan=2)
        self.tilt_speed_1.grid(row=2, column=6)
        self.pan_speed_1.grid(row=2, column=7, columnspan=2)
        self.ckbx_invert_tilt_1.grid(row=3, column=6)
        self.ckbx_invert_pan_1.grid(row=3, column=7, columnspan=2)

        # Grid the Overview Camera Controls
        self.btn_power_2.grid(row=0, column=0, padx=60)
        self.btn_ms_2.grid(row=1, column=0, padx=5, pady=5)
        self.btn_near_2.grid(row=0, column=2, padx=20, pady=10)
        self.btn_far_2.grid(row=1, column=2, padx=20, pady=10)
        self.btn_tele_2.grid(row=0, column=3, padx=20, pady=10)
        self.btn_wide_2.grid(row=1, column=3, padx=20, pady=10)
        self.label_camera_type_2.grid(row=2, column=0, columnspan=4)
        self.left_light_scale_2.grid(row=0, column=4, rowspan=3, padx=20, pady=5)
        self.right_light_scale_2.grid(row=0, column=5, rowspan=3, padx=45, pady=5)
        self.label_lights_2.grid(row=3, column=4, columnspan=2, padx=45, sticky=N)
        self.btn_tilt_up_2.grid(row=0, column=6, padx=20, pady=5)
        self.btn_tilt_down_2.grid(row=1, column=6, padx=20, pady=5)
        self.btn_pan_right_2.grid(row=0, column=8, padx=20, pady=5, rowspan=2)
        self.btn_pan_left_2.grid(row=0, column=7, padx=20, pady=5, rowspan=2)
        self.tilt_speed_2.grid(row=2, column=6)
        self.pan_speed_2.grid(row=2, column=7, columnspan=2)
        self.ckbx_invert_tilt_2.grid(row=3, column=6)
        self.ckbx_invert_pan_2.grid(row=3, column=7, columnspan=2)

        # Connect to Phidget Devices for Tool Camera
        self.power_1 = DigitalOutput()
        self.power_1.setDeviceSerialNumber(HUB2)
        self.power_1.setIsHubPortDevice(False)
        self.power_1.setHubPort(1)
        self.power_1.setChannel(0)
        try:
            self.power_1.openWaitForAttachment(1000)
        except PhidgetException as e:
            print("Failed to open (CAM POWER): " + e.details)

        self.manual_select_1 = DigitalOutput()
        self.manual_select_1.setDeviceSerialNumber(HUB2)
        self.manual_select_1.setIsHubPortDevice(False)
        self.manual_select_1.setHubPort(1)
        self.manual_select_1.setChannel(1)
        try:
            self.manual_select_1.openWaitForAttachment(1000)
        except PhidgetException as e:
            print("Failed to open (Manual Select): " + e.details)

        self.near_1 = DigitalOutput()
        self.near_1.setDeviceSerialNumber(HUB2)
        self.near_1.setIsHubPortDevice(False)
        self.near_1.setHubPort(1)
        self.near_1.setChannel(2)
        try:
            self.near_1.openWaitForAttachment(1000)
        except PhidgetException as e:
            print("Failed to open (NEAR): " + e.details)

        self.far_1 = DigitalOutput()
        self.far_1.setDeviceSerialNumber(HUB2)
        self.far_1.setIsHubPortDevice(False)
        self.far_1.setHubPort(1)
        self.far_1.setChannel(3)
        try:
            self.far_1.openWaitForAttachment(1000)
        except PhidgetException as e:
            print("Failed to open (FAR): " + e.details)

        self.wide_1 = DigitalOutput()
        self.wide_1.setDeviceSerialNumber(HUB2)
        self.wide_1.setIsHubPortDevice(False)
        self.wide_1.setHubPort(1)
        self.wide_1.setChannel(4)
        try:
            self.wide_1.openWaitForAttachment(1000)
        except PhidgetException as e:
            print("Failed to open (WIDE): " + e.details)

        self.tele_1 = DigitalOutput()
        self.tele_1.setDeviceSerialNumber(HUB2)
        self.tele_1.setIsHubPortDevice(False)
        self.tele_1.setHubPort(1)
        self.tele_1.setChannel(5)
        try:
            self.tele_1.openWaitForAttachment(1000)
        except PhidgetException as e:
            print("Failed to open (TELE): " + e.details)

        self.left_light_1 = VoltageOutput()
        self.left_light_1.setDeviceSerialNumber(HUB2)
        self.left_light_1.setIsHubPortDevice(False)
        self.left_light_1.setHubPort(2)
        self.left_light_1.setChannel(0)
        try:
            self.left_light_1.openWaitForAttachment(1000)
        except PhidgetException as e:
            print("Failed to open (LEFT LIGHT): " + e.details)

        self.right_light_1 = VoltageOutput()
        self.right_light_1.setDeviceSerialNumber(HUB2)
        self.right_light_1.setIsHubPortDevice(False)
        self.right_light_1.setHubPort(3)
        self.right_light_1.setChannel(0)
        try:
            self.right_light_1.openWaitForAttachment(1000)
        except PhidgetException as e:
            print("Failed to open (RIGHT LIGHT): " + e.details)

        self.pan_1 = VoltageOutput()
        self.pan_1.setDeviceSerialNumber(HUB2)
        self.pan_1.setIsHubPortDevice(False)
        self.pan_1.setHubPort(5)
        self.pan_1.setChannel(0)
        try:
            self.pan_1.openWaitForAttachment(1000)
        except PhidgetException as e:
            print("Failed to open (PAN): " + e.details)

        self.tilt_1 = VoltageOutput()
        self.tilt_1.setDeviceSerialNumber(HUB2)
        self.tilt_1.setIsHubPortDevice(False)
        self.tilt_1.setHubPort(4)
        self.tilt_1.setChannel(0)
        try:
            self.tilt_1.openWaitForAttachment(1000)
        except PhidgetException as e:
            print("Failed to open (TILT): " + e.details)

        self.btn_near_1.bind('<ButtonPress-1>', lambda event: self.focus_1("+"))
        self.btn_near_1.bind('<ButtonRelease-1>', lambda event: self.focus_1("0"))
        self.btn_far_1.bind('<ButtonPress-1>', lambda event: self.focus_1("-"))
        self.btn_far_1.bind('<ButtonRelease-1>', lambda event: self.focus_1("0"))
        self.btn_wide_1.bind('<ButtonPress-1>', lambda event: self.zoom_1("-"))
        self.btn_wide_1.bind('<ButtonRelease-1>', lambda event: self.zoom_1("0"))
        self.btn_tele_1.bind('<ButtonPress-1>', lambda event: self.zoom_1("+"))
        self.btn_tele_1.bind('<ButtonRelease-1>', lambda event: self.zoom_1("0"))
        self.btn_ms_1.bind('<ButtonPress-1>', lambda event: self.focus_type_1("ON"))
        self.btn_ms_1.bind('<ButtonRelease-1>', lambda event: self.focus_type_1("OFF"))

        self.btn_tilt_up_1.bind('<ButtonPress-1>', lambda event: self.tilt_move_1("-"))
        self.btn_tilt_up_1.bind('<ButtonRelease-1>', lambda event: self.tilt_move_1("0"))
        self.btn_tilt_down_1.bind('<ButtonPress-1>', lambda event: self.tilt_move_1("+"))
        self.btn_tilt_down_1.bind('<ButtonRelease-1>', lambda event: self.tilt_move_1("0"))
        self.btn_pan_right_1.bind('<ButtonPress-1>', lambda event: self.pan_move_1("R"))
        self.btn_pan_right_1.bind('<ButtonRelease-1>', lambda event: self.pan_move_1("0"))
        self.btn_pan_left_1.bind('<ButtonPress-1>', lambda event: self.pan_move_1("L"))
        self.btn_pan_left_1.bind('<ButtonRelease-1>', lambda event: self.pan_move_1("0"))

        # Connect to Phidget Devices for Overview Camera
        self.power_2 = DigitalOutput()
        self.power_2.setDeviceSerialNumber(HUB2)
        self.power_2.setIsHubPortDevice(False)
        self.power_2.setHubPort(1)
        self.power_2.setChannel(0)
        try:
            self.power_2.openWaitForAttachment(1000)
        except PhidgetException as e:
            print("Failed to open (CAM POWER): " + e.details)

        self.manual_select_2 = DigitalOutput()
        self.manual_select_2.setDeviceSerialNumber(HUB2)
        self.manual_select_2.setIsHubPortDevice(False)
        self.manual_select_2.setHubPort(1)
        self.manual_select_2.setChannel(1)
        try:
            self.manual_select_2.openWaitForAttachment(1000)
        except PhidgetException as e:
            print("Failed to open (Manual Select): " + e.details)

        self.near_2 = DigitalOutput()
        self.near_2.setDeviceSerialNumber(HUB2)
        self.near_2.setIsHubPortDevice(False)
        self.near_2.setHubPort(1)
        self.near_2.setChannel(2)
        try:
            self.near_2.openWaitForAttachment(1000)
        except PhidgetException as e:
            print("Failed to open (NEAR): " + e.details)

        self.far_2 = DigitalOutput()
        self.far_2.setDeviceSerialNumber(HUB2)
        self.far_2.setIsHubPortDevice(False)
        self.far_2.setHubPort(1)
        self.far_2.setChannel(3)
        try:
            self.far_2.openWaitForAttachment(1000)
        except PhidgetException as e:
            print("Failed to open (FAR): " + e.details)

        self.wide_2 = DigitalOutput()
        self.wide_2.setDeviceSerialNumber(HUB2)
        self.wide_2.setIsHubPortDevice(False)
        self.wide_2.setHubPort(1)
        self.wide_2.setChannel(4)
        try:
            self.wide_2.openWaitForAttachment(1000)
        except PhidgetException as e:
            print("Failed to open (WIDE): " + e.details)

        self.tele_2 = DigitalOutput()
        self.tele_2.setDeviceSerialNumber(HUB2)
        self.tele_2.setIsHubPortDevice(False)
        self.tele_2.setHubPort(1)
        self.tele_2.setChannel(5)
        try:
            self.tele_2.openWaitForAttachment(1000)
        except PhidgetException as e:
            print("Failed to open (TELE): " + e.details)

        self.left_light_2 = VoltageOutput()
        self.left_light_2.setDeviceSerialNumber(HUB2)
        self.left_light_2.setIsHubPortDevice(False)
        self.left_light_2.setHubPort(2)
        self.left_light_2.setChannel(0)
        try:
            self.left_light_2.openWaitForAttachment(1000)
        except PhidgetException as e:
            print("Failed to open (LEFT LIGHT): " + e.details)

        self.right_light_2 = VoltageOutput()
        self.right_light_2.setDeviceSerialNumber(HUB2)
        self.right_light_2.setIsHubPortDevice(False)
        self.right_light_2.setHubPort(3)
        self.right_light_2.setChannel(0)
        try:
            self.right_light_2.openWaitForAttachment(1000)
        except PhidgetException as e:
            print("Failed to open (RIGHT LIGHT): " + e.details)

        self.pan_2 = VoltageOutput()
        self.pan_2.setDeviceSerialNumber(HUB2)
        self.pan_2.setIsHubPortDevice(False)
        self.pan_2.setHubPort(5)
        self.pan_2.setChannel(0)
        try:
            self.pan_2.openWaitForAttachment(1000)
        except PhidgetException as e:
            print("Failed to open (PAN): " + e.details)

        self.tilt_2 = VoltageOutput()
        self.tilt_2.setDeviceSerialNumber(HUB2)
        self.tilt_2.setIsHubPortDevice(False)
        self.tilt_2.setHubPort(4)
        self.tilt_2.setChannel(0)
        try:
            self.tilt_2.openWaitForAttachment(1000)
        except PhidgetException as e:
            print("Failed to open (TILT): " + e.details)

    # Methods for Tool Camera
    def toggle_power_1(self):
        if self.power_1.getState() == True:
            self.power_1.setState(False)
            self.btn_power_1.config(bg="SystemButtonFace")
        elif self.power_1.getState() == False:
            self.power_1.setState(True)
            self.btn_power_1.config(bg=self.activeColor_1)

    def update_left_intensity_1(self, val):
        self.left_light_1.setVoltage(float(val))

    def update_right_intensity_1(self, val):
        self.right_light_1.setVoltage(float(val))

    def focus_1(self, direction):
        if direction == "+":
            self.near_1.setState(TRUE)
        elif direction == "-":
            self.far_1.setState(TRUE)
        elif direction == "0":
            self.far_1.setState(FALSE)
            self.near_1.setState(FALSE)

    def zoom_1(self, direction):
        if direction == "+":
            self.tele_1.setState(TRUE)
        elif direction == "-":
            self.wide_1.setState(TRUE)
        elif direction == "0":
            self.tele_1.setState(FALSE)
            self.wide_1.setState(FALSE)

    def pan_move_1(self, direction):
        voltage = float(self.pan_speed_1.get())
        if self.invert_pan_1.get():
            voltage *= -1
        if direction == "R":
            self.pan_1.setVoltage(voltage)
        elif direction == "L":
            self.pan_1.setVoltage(-1 * voltage)
        elif direction == "0":
            self.pan_1.setVoltage(0)

    def tilt_move_1(self, direction):
        voltage = float(self.tilt_speed_1.get())
        if self.invert_tilt_1.get():
            voltage *= -1
        if direction == "+":
            self.tilt_1.setVoltage(voltage)
        elif direction == "-":
            self.tilt_1.setVoltage(-1 * voltage)
        elif direction == "0":
            self.tilt_1.setVoltage(0)

    def focus_type_1(self, state):
        if state == "ON":
            self.manual_select_1.setState(True)
        elif state == "OFF":
            self.manual_select_1.setState(False)

    # Methods for Overview Camera
    def toggle_power_2(self):
        if self.power_2.getState() == True:
            self.power_2.setState(False)
            self.btn_power_2.config(bg="SystemButtonFace")
        elif self.power_2.getState() == False:
            self.power_2.setState(True)
            self.btn_power_2.config(bg=self.activeColor_2)

    def update_left_intensity_2(self, val):
        self.left_light_2.setVoltage(float(val))

    def update_right_intensity_2(self, val):
        self.right_light_2.setVoltage(float(val))

    def focus_2(self, direction):
        if direction == "+":
            self.near_2.setState(TRUE)
        elif direction == "-":
            self.far_2.setState(TRUE)
        elif direction == "0":
            self.far_2.setState(FALSE)
            self.near_2.setState(FALSE)

    def zoom_2(self, direction):
        if direction == "+":
            self.tele_2.setState(TRUE)
        elif direction == "-":
            self.wide_2.setState(TRUE)
        elif direction == "0":
            self.tele_2.setState(FALSE)
            self.wide_2.setState(FALSE)

    def pan_move_2(self, direction):
        voltage = float(self.pan_speed_2.get())
        if self.invert_pan_2.get():
            voltage *= -1
        if direction == "R":
            self.pan_2.setVoltage(voltage)
        elif direction == "L":
            self.pan_2.setVoltage(-1 * voltage)
        elif direction == "0":
            self.pan_2.setVoltage(0)

    def tilt_move_2(self, direction):
        voltage = float(self.tilt_speed_2.get())
        if self.invert_tilt_2.get():
            voltage *= -1
        if direction == "+":
            self.tilt_2.setVoltage(voltage)
        elif direction == "-":
            self.tilt_2.setVoltage(-1 * voltage)
        elif direction == "0":
            self.tilt_2.setVoltage(0)

    def focus_type_2(self, state):
        if state == "ON":
            self.manual_select_2.setState(True)
        elif state == "OFF":
            self.manual_select_2.setState(False)


root = Tk()
TIMC = MainWindow(root, SetupMainWindow())
root.mainloop()
