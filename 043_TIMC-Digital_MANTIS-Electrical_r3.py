###################################################################
# Tooling Inspection Motion Controller - Digital MANTIS Electrical
#
# Author: Timothy Clark
# Email: timothy.clark@ge.com
# Date: 07/27/2021
# Code Revision: 2
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
# Revision 2 Update:
#   Added another RJ overview camera.
#   Added exception for running the GUI offline.
#   Changed key binding definitions such that either camera may be operated via the gamepad.


from tkinter import *
from Phidget22.Devices.DCMotor import *
from Phidget22.Devices.CurrentInput import *
from Phidget22.Devices.DigitalOutput import *
from Phidget22.Devices.VoltageOutput import *
from Phidget22.Net import *

rainbow = ['SteelBlue1', 'DarkGoldenrod1', 'PaleGreen3', 'LightBlue3', 'DarkSlateGray3', 'MistyRose3', 'LightYellow3', 'dark khaki',
           'LightSalmon2', 'chocolate1']
blue_checkers = ['LightSkyBlue1', 'LightSkyBlue3', 'LightSkyBlue1', 'LightSkyBlue3', 'LightSkyBlue1', 'LightSkyBlue3', 'LightSkyBlue1',
                 'LightSkyBlue3', 'LightSkyBlue1', 'LightSkyBlue3']
green_checkers = ['DarkOliveGreen1', 'DarkOliveGreen4', 'DarkOliveGreen1', 'DarkOliveGreen4', 'DarkOliveGreen1', 'DarkOliveGreen4',
                  'DarkOliveGreen1', 'DarkOliveGreen4', 'DarkOliveGreen1', 'DarkOliveGreen4']
green_checkers2 = ['DarkOliveGreen3', 'DarkOliveGreen4', 'DarkOliveGreen3', 'DarkOliveGreen4', 'DarkOliveGreen3', 'DarkOliveGreen4',
                   'DarkOliveGreen3', 'DarkOliveGreen4', 'DarkOliveGreen3', 'DarkOliveGreen4']
gold_checkers = ['gold2', 'gold3', 'gold2', 'gold3', 'gold2', 'gold3', 'gold2', 'gold3', 'gold2', 'gold3', ]
orange_checkers = ['DarkOrange2', 'DarkOrange4', 'DarkOrange2', 'DarkOrange4', 'DarkOrange2', 'DarkOrange4', 'DarkOrange2', 'DarkOrange4',
                   'DarkOrange2', 'DarkOrange4', ]

# Vars for toggling Camera connection to gamepad.
game_pad_cam1 = False
game_pad_cam2 = False

# Line required to look for Phidget devices on the network
# Rev B Note: included exception for user to access the GUI without controller.

try:
    print('Connecting to Controller')
    Net.enableServerDiscovery(PhidgetServerType.PHIDGETSERVER_DEVICEREMOTE)
    Connected = True
except:
    Connected = False
    print('Connection Failed')
    print('Running in off-line mode.')

# TODO: GET REMAINING HUB SERIAL NUMBERS
# System A SN:040
# SN = "040"
# HUB1 = 539552
# HUB2 = 539066
# HUB3 = ??????

# System B
# SN = "041"
# HUB1 = 539079
# HUB2 = 539520
# HUB3 = ??????


# System C
# SN = "042"
# HUB1 = 539081
# HUB2 = 538800
# HUB3 = ??????

# System D
SN = "043"
HUB1 = 539155
HUB2 = 562466
HUB3 = 538798

# System E SN: 002
# SN = "044"
# HUB1 = 621065
# HUB2 = 621072
# HUB3 = 625954

# System F SN: 003
# SN = "045"
# HUB1 = 621098
# HUB2 = 621150
# HUB3 = 621170

# System TEST SN: 00X
# SN = "TEST"
# HUB1 = 666871
# HUB2 = 665948
# HUB3 = 671893

# Current Multiplier
MULT = 1


class SetupMainWindow:
    def __init__(self):
        self.gui_width = 1080
        self.gui_height = 650


class MainWindow:
    def __init__(self, master, parameters):
        self.parameters = parameters
        self.master = master
        self.master.geometry(str(parameters.gui_width) + "x" + str(parameters.gui_height))
        self.master.title("R3 - TIMC Digital MANTIS Electrical - S/N: " + SN)
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

        # Camera Movements
        # Revision B Note: Action on key strike for camera made more general in order to control mult. cameras.
        master.bind('<KeyPress-Left>', lambda event: self.out0.pan_move_gen("L"))
        master.bind('<KeyRelease-Left>', lambda event: self.out0.pan_move_gen("0"))
        master.bind('<KeyPress-Right>', lambda event: self.out0.pan_move_gen("R"))
        master.bind('<KeyRelease-Right>', lambda event: self.out0.pan_move_gen("0"))
        master.bind('<KeyPress-Up>', lambda event: self.out0.tilt_move_gen("-"))
        master.bind('<KeyRelease-Up>', lambda event: self.out0.tilt_move_gen("0"))
        master.bind('<KeyPress-Down>', lambda event: self.out0.tilt_move_gen("+"))
        master.bind('<KeyRelease-Down>', lambda event: self.out0.tilt_move_gen("0"))

        master.bind('<KeyPress-plus>', lambda event: self.out0.zoom_gen("+"))
        master.bind('<KeyRelease-plus>', lambda event: self.out0.zoom_gen("0"))
        master.bind('<KeyPress-minus>', lambda event: self.out0.zoom_gen("-"))
        master.bind('<KeyRelease-minus>', lambda event: self.out0.zoom_gen("0"))

        master.bind('<KeyPress-Insert>', lambda event: self.out0.focus_gen("+"))
        master.bind('<KeyRelease-Insert>', lambda event: self.out0.focus_gen("0"))
        master.bind('<KeyPress-Delete>', lambda event: self.out0.focus_gen("-"))
        master.bind('<KeyRelease-Delete>', lambda event: self.out0.focus_gen("0"))

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

        # Rev 2 Note: Adding a section to prevent a runaway condition
        master.bind('<FocusOut>', lambda event: self.all_stop())

    def all_stop(self):
        print('\n \n User has navigated away from interface\n    Stopping all axis movement \n \n')
        self.out0.out1.jog("0")
        self.out0.out2.jog("0")
        self.out0.out3.jog("0")
        self.out0.out4.jog("0")
        self.out0.out5.jog("0")
        self.out0.out6.jog("0")
        self.out0.out7.jog("0")
        self.out0.pan_move_gen("0")
        self.out0.tilt_move_gen("0")


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
        self.speed = Scale(frame, orient=HORIZONTAL, from_=0.01, to=1, resolution=.01, bg=color, label="      Axis Speed",
                           highlightthickness=0)
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

        # TIMC added to measure if the user has been stressing out the VART vert motor too long
        self.current_timer = None
        self.motor_locked_out = False

        # Connect to Phidget Motor Driver
        try:
            self.axis = DCMotor()
            self.axis.setDeviceSerialNumber(serial_number)
            self.axis.setIsHubPortDevice(False)
            self.axis.setHubPort(port)
            self.axis.setChannel(0)
            self.axis.openWaitForAttachment(5000)
            self.axis.setAcceleration(self.acceleration)
            self.axis.setCurrentLimit(self.current_limit)   # TIMC bug found in which all motors have 2A limit until config window is opened

            self.axis_current = CurrentInput()
            self.axis_current.setDeviceSerialNumber(serial_number)
            self.axis_current.setIsHubPortDevice(False)
            self.axis_current.setHubPort(port)
            self.axis_current.setChannel(0)
            self.axis_current.openWaitForAttachment(5000)
            self.axis_current.setDataInterval(100)  # TIMC updated from 200 to 100
            self.axis_current.setCurrentChangeTrigger(0.0)
            self.current_data_points = []  # TIMC moving average of current values final size to be 10
            # With the update interval being 100 ms, the call handler for current change should not be attached until data is ready
            root.after(100, self.init_current_readings)

            # Bind user button press of jog button to movement method
            self.jog_pos_btn.bind('<ButtonPress-1>', lambda event: self.jog("+"))
            self.jog_pos_btn.bind('<ButtonRelease-1>', lambda event: self.jog("0"))
            self.jog_neg_btn.bind('<ButtonPress-1>', lambda event: self.jog("-"))
            self.jog_neg_btn.bind('<ButtonRelease-1>', lambda event: self.jog("0"))
        except:
            print('Running in off-line mode.')

    # TIMC handler must be started after the main loop starts
    def init_current_readings(self):
        self.axis_current.setOnCurrentChangeHandler(self.update_current)

    def jog(self, direction):
        # Calculate the speed as a percentage of the maximum velocity
        velocity = float(self.speed.get()) * self.max_velocity
        # Apply invert if necessary
        if self.invert == TRUE:
            velocity *= -1

        # Command Movement
        if direction == "+":
            if not self.motor_locked_out:
                self.axis.setTargetVelocity(velocity)
        elif direction == "-":
            if not self.motor_locked_out:
                self.axis.setTargetVelocity(-1 * velocity)
        elif direction == "0":
            self.axis.setTargetVelocity(0)

    def update_current(self, trash, value):
        list_length = len(self.current_data_points)
        # Calculate the moving average over 10 points
        if list_length == 10:
            self.current_data_points.pop(0)
            self.current_data_points.append(value)
            new_average = sum(self.current_data_points) / 10
        else:
            self.current_data_points.append(value)
            new_average = sum(self.current_data_points) / (list_length + 1)
        # Reset the over current timer if the current is below half the allowable limit
        if abs(new_average) < abs(0.5 * self.current_limit):
            self.reset_current_timer()
        self.current_text.set(abs(round(new_average, 3)))

    def reset_current_timer(self):
        if self.current_timer is not None:
            root.after_cancel(self.current_timer)
        # Set a timer that will expire after 3 seconds of the user commanding a high current condition
        self.current_timer = root.after(3000, self.init_motor_lockout)

    def init_motor_lockout(self):
        self.motor_locked_out = True
        self.axis.setTargetVelocity(0)
        self.jog_pos_btn.configure(background="red")
        self.jog_neg_btn.configure(background="red")
        root.after(8000, self.disable_motor_lockout)

    def disable_motor_lockout(self):
        self.motor_locked_out = False
        self.jog_pos_btn.configure(background="light grey")
        self.jog_neg_btn.configure(background="light grey")

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
        camera1_frame = Frame(master, borderwidth=2, relief=SUNKEN)
        camera2_frame = Frame(master, borderwidth=2, relief=SUNKEN)

        frame1.grid(row=1, column=0)
        frame2.grid(row=1, column=1)
        frame3.grid(row=1, column=2)
        frame4.grid(row=1, column=3)
        frame5.grid(row=1, column=4)
        frame6.grid(row=1, column=5)
        frame7.grid(row=1, column=6)
        camera1_frame.grid(row=3, column=0, columnspan=7, sticky=W)
        camera2_frame.grid(row=7, column=0, columnspan=7, sticky=W)

        self.out1 = AxisFrame(frame1, "BASE CIRC", "VESSEL RIGHT", "VESSEL LEFT", HUB1, 5, colorArray[0], 3.3, 0.55)
        self.out2 = AxisFrame(frame2, "BASE AUX", "CW/IN", "CCW/OUT", HUB2, 0, colorArray[1], 2.2, 0.11)
        self.out3 = AxisFrame(frame3, "VARD ROT", "CW", "CCW", HUB1, 3, colorArray[2], 2.2, 0.15)
        self.out4 = AxisFrame(frame4, "VARD VERT", "UP", "DOWN", HUB1, 4, colorArray[3], 7.8, 0.54)
        self.out5 = AxisFrame(frame5, "DA MAST", "UP", "DOWN", HUB1, 0, colorArray[4], 8, 0.86)
        self.out6 = AxisFrame(frame6, "DA PAN", "CW", "CCW", HUB1, 2, colorArray[5], 3.0, 0.30)
        self.out7 = AxisFrame(frame7, "DA TILT", "UP", "DOWN", HUB1, 1, colorArray[6], 3.6, 0.57)
        camera1_frame.config(bg=colorArray[7])
        camera2_frame.config(bg=colorArray[8])

        # RJ Camera1 Control Code
        self.invert_tilt_cam1 = BooleanVar()
        self.invert_pan_cam1 = BooleanVar()
        self.game_pad_cam1 = BooleanVar()
        self.btn_power_cam1 = Button(camera1_frame, text="PWR", font="Courier, 12", command=self.toggle_power_cam1)
        self.btn_near_cam1 = Button(camera1_frame, text="NEAR", font="Courier, 12", width=7)
        self.btn_far_cam1 = Button(camera1_frame, text="FAR", font="Courier, 12", width=7)
        self.btn_wide_cam1 = Button(camera1_frame, text="WIDE", font="Courier, 12", width=7)
        self.btn_tele_cam1 = Button(camera1_frame, text="TELE", font="Courier, 12", width=7)
        self.btn_ms_cam1 = Button(camera1_frame, text="MS", font="Courier, 12", width=7)
        self.left_light_scale_cam1 = Scale(camera1_frame, orient=VERTICAL, from_=0, to=0.45, resolution=0.01,
                                           command=self.update_left_intensity_cam1, bg=colorArray[7], highlightthickness=0)
        self.right_light_scale_cam1 = Scale(camera1_frame, orient=VERTICAL, from_=0, to=0.45, resolution=0.01,
                                            command=self.update_right_intensity_cam1, bg=colorArray[7], highlightthickness=0)
        self.label_lights_cam1 = Label(camera1_frame, text="  Light Intensity", bg=colorArray[7])
        self.btn_tilt_up_cam1 = Button(camera1_frame, text="TILT UP", font="Courier, 12", width=10)
        self.btn_tilt_down_cam1 = Button(camera1_frame, text="TILT DOWN", font="Courier, 12", width=10)
        self.btn_pan_right_cam1 = Button(camera1_frame, text="PAN RIGHT", font="Courier, 12", width=10)
        self.btn_pan_left_cam1 = Button(camera1_frame, text="PAN LEFT", font="Courier, 12", width=10)
        self.tilt_speed_cam1 = Scale(camera1_frame, orient=HORIZONTAL, from_=0.01, to=.5, resolution=0.01, bg=colorArray[7],
                                     highlightthickness=0)
        self.pan_speed_cam1 = Scale(camera1_frame, orient=HORIZONTAL, from_=0.01, to=.5, resolution=0.01, bg=colorArray[7],
                                    highlightthickness=0)
        self.ckbx_invert_tilt_cam1 = Checkbutton(camera1_frame, text="Invert Tilt", variable=self.invert_tilt_cam1, bg=colorArray[7])
        self.ckbx_invert_pan_cam1 = Checkbutton(camera1_frame, text="Invert Pan", variable=self.invert_pan_cam1, bg=colorArray[7])
        self.activeColor = 'SpringGreen4'
        self.label_cam1 = Label(camera1_frame, text="      TOOL      \nCAMERA", font="Courier, 12", bg=colorArray[7])
        self.ckbx_gamepad_cam1 = Checkbutton(camera1_frame, text="Enable Gamepad", variable=self.game_pad_cam1, bg=colorArray[7],
                                             command=self.game_pad_link_cam1)

        self.tilt_speed_cam1.set(0.15)
        self.pan_speed_cam1.set(0.15)

        self.btn_power_cam1.grid(row=0, column=0, padx=60)
        self.btn_ms_cam1.grid(row=1, column=0, padx=5, pady=5)
        self.btn_near_cam1.grid(row=0, column=2, padx=20, pady=10)
        self.btn_far_cam1.grid(row=1, column=2, padx=20, pady=10)
        self.btn_tele_cam1.grid(row=0, column=3, padx=20, pady=10)
        self.btn_wide_cam1.grid(row=1, column=3, padx=20, pady=10)
        self.left_light_scale_cam1.grid(row=0, column=4, rowspan=3, padx=20, pady=5)
        self.right_light_scale_cam1.grid(row=0, column=5, rowspan=3, padx=45, pady=5)
        self.label_lights_cam1.grid(row=3, column=4, columnspan=2, padx=45, sticky=N)
        self.btn_tilt_up_cam1.grid(row=0, column=6, padx=20, pady=5)
        self.btn_tilt_down_cam1.grid(row=1, column=6, padx=20, pady=5)
        self.btn_pan_right_cam1.grid(row=0, column=8, padx=20, pady=5, rowspan=2)
        self.btn_pan_left_cam1.grid(row=0, column=7, padx=20, pady=5, rowspan=2)
        self.tilt_speed_cam1.grid(row=2, column=6)
        self.pan_speed_cam1.grid(row=2, column=7, columnspan=2)
        self.ckbx_invert_tilt_cam1.grid(row=3, column=6)
        self.ckbx_invert_pan_cam1.grid(row=3, column=7, columnspan=2)
        self.label_cam1.grid(row=3, column=0, columnspan=2, padx=50, sticky=N)
        self.ckbx_gamepad_cam1.grid(row=3, column=1, columnspan=2)

        # RJ Camera2 Control Code
        self.invert_tilt_cam2 = BooleanVar()
        self.invert_pan_cam2 = BooleanVar()
        self.game_pad_cam2 = BooleanVar()
        self.btn_power_cam2 = Button(camera2_frame, text="PWR", font="Courier, 12", command=self.toggle_power_cam2)
        self.btn_near_cam2 = Button(camera2_frame, text="NEAR", font="Courier, 12", width=7)
        self.btn_far_cam2 = Button(camera2_frame, text="FAR", font="Courier, 12", width=7)
        self.btn_wide_cam2 = Button(camera2_frame, text="WIDE", font="Courier, 12", width=7)
        self.btn_tele_cam2 = Button(camera2_frame, text="TELE", font="Courier, 12", width=7)
        self.btn_ms_cam2 = Button(camera2_frame, text="MS", font="Courier, 12", width=7)
        self.left_light_scale_cam2 = Scale(camera2_frame, orient=VERTICAL, from_=0, to=0.45, resolution=0.01,
                                           command=self.update_left_intensity_cam2, highlightthickness=0, bg=colorArray[8])
        self.right_light_scale_cam2 = Scale(camera2_frame, orient=VERTICAL, from_=0, to=0.45, resolution=0.01,
                                            command=self.update_right_intensity_cam2, highlightthickness=0, bg=colorArray[8])
        self.label_lights_cam2 = Label(camera2_frame, text="  Light Intensity", bg=colorArray[8])
        self.btn_tilt_up_cam2 = Button(camera2_frame, text="TILT UP", font="Courier, 12", width=10)
        self.btn_tilt_down_cam2 = Button(camera2_frame, text="TILT DOWN", font="Courier, 12", width=10)
        self.btn_pan_right_cam2 = Button(camera2_frame, text="PAN RIGHT", font="Courier, 12", width=10)
        self.btn_pan_left_cam2 = Button(camera2_frame, text="PAN LEFT", font="Courier, 12", width=10)
        self.tilt_speed_cam2 = Scale(camera2_frame, orient=HORIZONTAL, from_=0.01, to=.5, resolution=0.01, highlightthickness=0,
                                     bg=colorArray[8])
        self.pan_speed_cam2 = Scale(camera2_frame, orient=HORIZONTAL, from_=0.01, to=.5, resolution=0.01, highlightthickness=0,
                                    bg=colorArray[8])
        self.ckbx_invert_tilt_cam2 = Checkbutton(camera2_frame, text="Invert Tilt", variable=self.invert_tilt_cam2, bg=colorArray[8])
        self.ckbx_invert_pan_cam2 = Checkbutton(camera2_frame, text="Invert Pan", variable=self.invert_pan_cam2, bg=colorArray[8])
        self.activeColor = 'SpringGreen4'
        self.label_cam2 = Label(camera2_frame, text="OVER VIEW\nCAMERA", font="Courier, 12", bg=colorArray[8])
        self.ckbx_gamepad_cam2 = Checkbutton(camera2_frame, text="Enable Gamepad", variable=self.game_pad_cam2, bg=colorArray[8],
                                             command=self.game_pad_link_cam2)

        self.tilt_speed_cam2.set(0.15)
        self.pan_speed_cam2.set(0.15)

        self.btn_power_cam2.grid(row=0, column=0, padx=60)
        self.btn_ms_cam2.grid(row=1, column=0, padx=5, pady=5)
        self.btn_near_cam2.grid(row=0, column=2, padx=20, pady=10)
        self.btn_far_cam2.grid(row=1, column=2, padx=20, pady=10)
        self.btn_tele_cam2.grid(row=0, column=3, padx=20, pady=10)
        self.btn_wide_cam2.grid(row=1, column=3, padx=20, pady=10)
        self.left_light_scale_cam2.grid(row=0, column=4, rowspan=3, padx=20, pady=5)
        self.right_light_scale_cam2.grid(row=0, column=5, rowspan=3, padx=45, pady=5)
        self.label_lights_cam2.grid(row=3, column=4, columnspan=2, padx=45, sticky=N)
        self.btn_tilt_up_cam2.grid(row=0, column=6, padx=20, pady=5)
        self.btn_tilt_down_cam2.grid(row=1, column=6, padx=20, pady=5)
        self.btn_pan_right_cam2.grid(row=0, column=8, padx=20, pady=5, rowspan=2)
        self.btn_pan_left_cam2.grid(row=0, column=7, padx=20, pady=5, rowspan=2)
        self.tilt_speed_cam2.grid(row=2, column=6)
        self.pan_speed_cam2.grid(row=2, column=7, columnspan=2)
        self.ckbx_invert_tilt_cam2.grid(row=3, column=6)
        self.ckbx_invert_pan_cam2.grid(row=3, column=7, columnspan=2)
        self.label_cam2.grid(row=3, column=0, columnspan=2, padx=50, sticky=N)
        self.ckbx_gamepad_cam2.grid(row=3, column=1, columnspan=2)

        # Connect to Phidget Devices
        # CAMERA 1 COMMANDS
        try:
            self.power_cam1 = DigitalOutput()
            self.power_cam1.setDeviceSerialNumber(HUB2)
            self.power_cam1.setIsHubPortDevice(False)
            self.power_cam1.setHubPort(1)
            self.power_cam1.setChannel(0)
            self.power_cam1.openWaitForAttachment(5000)

            self.manual_select_cam1 = DigitalOutput()
            self.manual_select_cam1.setDeviceSerialNumber(HUB2)
            self.manual_select_cam1.setIsHubPortDevice(False)
            self.manual_select_cam1.setHubPort(1)
            self.manual_select_cam1.setChannel(1)
            self.manual_select_cam1.openWaitForAttachment(5000)

            self.near_cam1 = DigitalOutput()
            self.near_cam1.setDeviceSerialNumber(HUB2)
            self.near_cam1.setIsHubPortDevice(False)
            self.near_cam1.setHubPort(1)
            self.near_cam1.setChannel(2)
            self.near_cam1.openWaitForAttachment(5000)

            self.far_cam1 = DigitalOutput()
            self.far_cam1.setDeviceSerialNumber(HUB2)
            self.far_cam1.setIsHubPortDevice(False)
            self.far_cam1.setHubPort(1)
            self.far_cam1.setChannel(3)
            self.far_cam1.openWaitForAttachment(5000)
            self.wide_cam1 = DigitalOutput()
            self.wide_cam1.setDeviceSerialNumber(HUB2)
            self.wide_cam1.setIsHubPortDevice(False)
            self.wide_cam1.setHubPort(1)
            self.wide_cam1.setChannel(4)
            self.wide_cam1.openWaitForAttachment(5000)

            self.tele_cam1 = DigitalOutput()
            self.tele_cam1.setDeviceSerialNumber(HUB2)
            self.tele_cam1.setIsHubPortDevice(False)
            self.tele_cam1.setHubPort(1)
            self.tele_cam1.setChannel(5)
            self.tele_cam1.openWaitForAttachment(5000)

            self.left_light_cam1 = VoltageOutput()
            self.left_light_cam1.setDeviceSerialNumber(HUB2)
            self.left_light_cam1.setIsHubPortDevice(False)
            self.left_light_cam1.setHubPort(2)
            self.left_light_cam1.setChannel(0)
            self.left_light_cam1.openWaitForAttachment(5000)

            self.right_light_cam1 = VoltageOutput()
            self.right_light_cam1.setDeviceSerialNumber(HUB2)
            self.right_light_cam1.setIsHubPortDevice(False)
            self.right_light_cam1.setHubPort(3)
            self.right_light_cam1.setChannel(0)
            self.right_light_cam1.openWaitForAttachment(5000)

            self.pan_cam1 = VoltageOutput()
            self.pan_cam1.setDeviceSerialNumber(HUB2)
            self.pan_cam1.setIsHubPortDevice(False)
            self.pan_cam1.setHubPort(5)
            self.pan_cam1.setChannel(0)
            self.pan_cam1.openWaitForAttachment(5000)

            self.tilt_cam1 = VoltageOutput()
            self.tilt_cam1.setDeviceSerialNumber(HUB2)
            self.tilt_cam1.setIsHubPortDevice(False)
            self.tilt_cam1.setHubPort(4)
            self.tilt_cam1.setChannel(0)
            self.tilt_cam1.openWaitForAttachment(5000)
        except:
            print('Running in off-line mode.')

        # CAMERA 2 COMMANDS
        try:
            self.power_cam2 = DigitalOutput()
            self.power_cam2.setDeviceSerialNumber(HUB3)
            self.power_cam2.setIsHubPortDevice(False)
            self.power_cam2.setHubPort(1)
            self.power_cam2.setChannel(0)
            self.power_cam2.openWaitForAttachment(5000)

            self.manual_select_cam2 = DigitalOutput()
            self.manual_select_cam2.setDeviceSerialNumber(HUB3)
            self.manual_select_cam2.setIsHubPortDevice(False)
            self.manual_select_cam2.setHubPort(1)
            self.manual_select_cam2.setChannel(1)
            self.manual_select_cam2.openWaitForAttachment(5000)

            self.near_cam2 = DigitalOutput()
            self.near_cam2.setDeviceSerialNumber(HUB3)
            self.near_cam2.setIsHubPortDevice(False)
            self.near_cam2.setHubPort(1)
            self.near_cam2.setChannel(2)
            self.near_cam2.openWaitForAttachment(5000)

            self.far_cam2 = DigitalOutput()
            self.far_cam2.setDeviceSerialNumber(HUB3)
            self.far_cam2.setIsHubPortDevice(False)
            self.far_cam2.setHubPort(1)
            self.far_cam2.setChannel(3)
            self.far_cam2.openWaitForAttachment(5000)
            self.wide_cam2 = DigitalOutput()
            self.wide_cam2.setDeviceSerialNumber(HUB3)
            self.wide_cam2.setIsHubPortDevice(False)
            self.wide_cam2.setHubPort(1)
            self.wide_cam2.setChannel(4)
            self.wide_cam2.openWaitForAttachment(5000)

            self.tele_cam2 = DigitalOutput()
            self.tele_cam2.setDeviceSerialNumber(HUB3)
            self.tele_cam2.setIsHubPortDevice(False)
            self.tele_cam2.setHubPort(1)
            self.tele_cam2.setChannel(5)
            self.tele_cam2.openWaitForAttachment(5000)

            self.left_light_cam2 = VoltageOutput()
            self.left_light_cam2.setDeviceSerialNumber(HUB3)
            self.left_light_cam2.setIsHubPortDevice(False)
            self.left_light_cam2.setHubPort(2)
            self.left_light_cam2.setChannel(0)
            self.left_light_cam2.openWaitForAttachment(5000)

            self.right_light_cam2 = VoltageOutput()
            self.right_light_cam2.setDeviceSerialNumber(HUB3)
            self.right_light_cam2.setIsHubPortDevice(False)
            self.right_light_cam2.setHubPort(3)
            self.right_light_cam2.setChannel(0)
            self.right_light_cam2.openWaitForAttachment(5000)

            self.pan_cam2 = VoltageOutput()
            self.pan_cam2.setDeviceSerialNumber(HUB3)
            self.pan_cam2.setIsHubPortDevice(False)
            self.pan_cam2.setHubPort(5)
            self.pan_cam2.setChannel(0)
            self.pan_cam2.openWaitForAttachment(5000)

            self.tilt_cam2 = VoltageOutput()
            self.tilt_cam2.setDeviceSerialNumber(HUB3)
            self.tilt_cam2.setIsHubPortDevice(False)
            self.tilt_cam2.setHubPort(4)
            self.tilt_cam2.setChannel(0)
            self.tilt_cam2.openWaitForAttachment(5000)
        except:
            print('Running in off-line mode.')

        # Camera 1 button binding:
        self.btn_near_cam1.bind('<ButtonPress-1>', lambda event: self.focus_cam1("+"))
        self.btn_near_cam1.bind('<ButtonRelease-1>', lambda event: self.focus_cam1("0"))
        self.btn_far_cam1.bind('<ButtonPress-1>', lambda event: self.focus_cam1("-"))
        self.btn_far_cam1.bind('<ButtonRelease-1>', lambda event: self.focus_cam1("0"))
        self.btn_wide_cam1.bind('<ButtonPress-1>', lambda event: self.zoom_cam1("-"))
        self.btn_wide_cam1.bind('<ButtonRelease-1>', lambda event: self.zoom_cam1("0"))
        self.btn_tele_cam1.bind('<ButtonPress-1>', lambda event: self.zoom_cam1("+"))
        self.btn_tele_cam1.bind('<ButtonRelease-1>', lambda event: self.zoom_cam1("0"))
        self.btn_ms_cam1.bind('<ButtonPress-1>', lambda event: self.focus_type_cam1("ON"))
        self.btn_ms_cam1.bind('<ButtonRelease-1>', lambda event: self.focus_type_cam1("OFF"))
        self.btn_tilt_up_cam1.bind('<ButtonPress-1>', lambda event: self.tilt_move_cam1("-"))
        self.btn_tilt_up_cam1.bind('<ButtonRelease-1>', lambda event: self.tilt_move_cam1("0"))
        self.btn_tilt_down_cam1.bind('<ButtonPress-1>', lambda event: self.tilt_move_cam1("+"))
        self.btn_tilt_down_cam1.bind('<ButtonRelease-1>', lambda event: self.tilt_move_cam1("0"))
        self.btn_pan_right_cam1.bind('<ButtonPress-1>', lambda event: self.pan_move_cam1("R"))
        self.btn_pan_right_cam1.bind('<ButtonRelease-1>', lambda event: self.pan_move_cam1("0"))
        self.btn_pan_left_cam1.bind('<ButtonPress-1>', lambda event: self.pan_move_cam1("L"))
        self.btn_pan_left_cam1.bind('<ButtonRelease-1>', lambda event: self.pan_move_cam1("0"))

        # Camera 2 button binding:
        self.btn_near_cam2.bind('<ButtonPress-1>', lambda event: self.focus_cam2("+"))
        self.btn_near_cam2.bind('<ButtonRelease-1>', lambda event: self.focus_cam2("0"))
        self.btn_far_cam2.bind('<ButtonPress-1>', lambda event: self.focus_cam2("-"))
        self.btn_far_cam2.bind('<ButtonRelease-1>', lambda event: self.focus_cam2("0"))
        self.btn_wide_cam2.bind('<ButtonPress-1>', lambda event: self.zoom_cam2("-"))
        self.btn_wide_cam2.bind('<ButtonRelease-1>', lambda event: self.zoom_cam2("0"))
        self.btn_tele_cam2.bind('<ButtonPress-1>', lambda event: self.zoom_cam2("+"))
        self.btn_tele_cam2.bind('<ButtonRelease-1>', lambda event: self.zoom_cam2("0"))
        self.btn_ms_cam2.bind('<ButtonPress-1>', lambda event: self.focus_type_cam2("ON"))
        self.btn_ms_cam2.bind('<ButtonRelease-1>', lambda event: self.focus_type_cam2("OFF"))
        self.btn_tilt_up_cam2.bind('<ButtonPress-1>', lambda event: self.tilt_move_cam2("-"))
        self.btn_tilt_up_cam2.bind('<ButtonRelease-1>', lambda event: self.tilt_move_cam2("0"))
        self.btn_tilt_down_cam2.bind('<ButtonPress-1>', lambda event: self.tilt_move_cam2("+"))
        self.btn_tilt_down_cam2.bind('<ButtonRelease-1>', lambda event: self.tilt_move_cam2("0"))
        self.btn_pan_right_cam2.bind('<ButtonPress-1>', lambda event: self.pan_move_cam2("R"))
        self.btn_pan_right_cam2.bind('<ButtonRelease-1>', lambda event: self.pan_move_cam2("0"))
        self.btn_pan_left_cam2.bind('<ButtonPress-1>', lambda event: self.pan_move_cam2("L"))
        self.btn_pan_left_cam2.bind('<ButtonRelease-1>', lambda event: self.pan_move_cam2("0"))

    # Un-necessary, but nice to have.
    def game_pad_link_cam1(self):
        self.game_pad_cam2.set(False)
        if self.game_pad_cam1.get():
            print('Camera 1 is connected to the gamepad.')
        else:
            print('Camera 1 is dis-connected from the gamepad.')

    # Camera 1 definitions:
    def toggle_power_cam1(self):
        if self.power_cam1.getState() == True:
            self.power_cam1.setState(False)
            self.btn_power_cam1.config(bg="SystemButtonFace")
        elif self.power_cam1.getState() == False:
            self.power_cam1.setState(True)
            self.btn_power_cam1.config(bg=self.activeColor)

    def update_left_intensity_cam1(self, val):
        self.left_light_cam1.setVoltage(float(val))

    def update_right_intensity_cam1(self, val):
        self.right_light_cam1.setVoltage(float(val))

    def focus_cam1(self, direction):
        if direction == "+":
            self.near_cam1.setState(TRUE)
        elif direction == "-":
            self.far_cam1.setState(TRUE)
        elif direction == "0":
            self.far_cam1.setState(FALSE)
            self.near_cam1.setState(FALSE)

    def zoom_cam1(self, direction):
        if direction == "+":
            self.tele_cam1.setState(TRUE)
        elif direction == "-":
            self.wide_cam1.setState(TRUE)
        elif direction == "0":
            self.tele_cam1.setState(FALSE)
            self.wide_cam1.setState(FALSE)

    def pan_move_cam1(self, direction):
        voltage = float(self.pan_speed_cam1.get())
        if self.invert_pan_cam1.get():
            voltage *= -1
        if direction == "R":
            self.pan_cam1.setVoltage(voltage)
        elif direction == "L":
            self.pan_cam1.setVoltage(-1 * voltage)
            print('camera 1 panning left :)')
        elif direction == "0":
            self.pan_cam1.setVoltage(0)

    def tilt_move_cam1(self, direction):
        voltage = float(self.tilt_speed_cam1.get())
        if self.invert_tilt_cam1.get():
            voltage *= -1
        if direction == "+":
            self.tilt_cam1.setVoltage(voltage)
        elif direction == "-":
            self.tilt_cam1.setVoltage(-1 * voltage)
        elif direction == "0":
            self.tilt_cam1.setVoltage(0)

    def focus_type_cam1(self, state):
        if state == "ON":
            self.manual_select_cam1.setState(True)
        elif state == "OFF":
            self.manual_select_cam1.setState(False)

    # Camera 2 definitions:
    def toggle_power_cam2(self):
        if self.power_cam2.getState() == True:
            self.power_cam2.setState(False)
            self.btn_power_cam2.config(bg="SystemButtonFace")
        elif self.power_cam2.getState() == False:
            self.power_cam2.setState(True)
            self.btn_power_cam2.config(bg=self.activeColor)

    def update_left_intensity_cam2(self, val):
        self.left_light_cam2.setVoltage(float(val))

    def update_right_intensity_cam2(self, val):
        self.right_light_cam2.setVoltage(float(val))

    def focus_cam2(self, direction):
        if direction == "+":
            self.near_cam2.setState(TRUE)
        elif direction == "-":
            self.far_cam2.setState(TRUE)
        elif direction == "0":
            self.far_cam2.setState(FALSE)
            self.near_cam2.setState(FALSE)

    def zoom_cam2(self, direction):
        if direction == "+":
            self.tele_cam2.setState(TRUE)
        elif direction == "-":
            self.wide_cam2.setState(TRUE)
        elif direction == "0":
            self.tele_cam2.setState(FALSE)
            self.wide_cam2.setState(FALSE)

    def pan_move_cam2(self, direction):
        voltage = float(self.pan_speed_cam2.get())
        if self.invert_pan_cam2.get():
            voltage *= -1
        if direction == "R":
            self.pan_cam2.setVoltage(voltage)
        elif direction == "L":
            self.pan_cam2.setVoltage(-1 * voltage)
        elif direction == "0":
            self.pan_cam2.setVoltage(0)

    def tilt_move_cam2(self, direction):
        voltage = float(self.tilt_speed_cam2.get())
        if self.invert_tilt_cam2.get():
            voltage *= -1
        if direction == "+":
            self.tilt_cam2.setVoltage(voltage)
        elif direction == "-":
            self.tilt_cam2.setVoltage(-1 * voltage)
        elif direction == "0":
            self.tilt_cam2.setVoltage(0)

    def focus_type_cam2(self, state):
        if state == "ON":
            self.manual_select_cam2.setState(True)
        elif state == "OFF":
            self.manual_select_cam2.setState(False)

    # Un-neccesary, but nice to have the notice.
    def game_pad_link_cam2(self):
        self.game_pad_cam1.set(False)
        if self.game_pad_cam2.get():
            print('Camera 2 is connected to the gamepad.')
        else:
            print('Camera 2 is dis-connected from the gamepad.')

    def focus_gen(self, direction):
        if self.game_pad_cam1.get():
            if direction == "+":
                self.near_cam1.setState(TRUE)
            elif direction == "-":
                self.far_cam1.setState(TRUE)
            elif direction == "0":
                self.far_cam1.setState(FALSE)
                self.near_cam1.setState(FALSE)
        if self.game_pad_cam2.get():
            if direction == "+":
                self.near_cam2.setState(TRUE)
            elif direction == "-":
                self.far_cam2.setState(TRUE)
            elif direction == "0":
                self.far_cam2.setState(FALSE)
                self.near_cam2.setState(FALSE)

    def zoom_gen(self, direction):
        if self.game_pad_cam1.get():
            if direction == "+":
                self.tele_cam1.setState(TRUE)
            elif direction == "-":
                self.wide_cam1.setState(TRUE)
            elif direction == "0":
                self.tele_cam1.setState(FALSE)
                self.wide_cam1.setState(FALSE)
        if self.game_pad_cam2.get():
            if direction == "+":
                self.tele_cam2.setState(TRUE)
            elif direction == "-":
                self.wide_cam2.setState(TRUE)
            elif direction == "0":
                self.tele_cam2.setState(FALSE)
                self.wide_cam2.setState(FALSE)

    def pan_move_gen(self, direction):
        if self.game_pad_cam1.get():
            voltage = float(self.pan_speed_cam1.get())
            if self.invert_pan_cam1.get():
                voltage *= -1
            if direction == "R":
                self.pan_cam1.setVoltage(voltage)
            elif direction == "L":
                self.pan_cam1.setVoltage(-1 * voltage)
            elif direction == "0":
                self.pan_cam1.setVoltage(0)
        if self.game_pad_cam2.get():
            voltage = float(self.pan_speed_cam2.get())
            if self.invert_pan_cam1.get():
                voltage *= -1
            if direction == "R":
                self.pan_cam2.setVoltage(voltage)
            elif direction == "L":
                self.pan_cam2.setVoltage(-1 * voltage)
            elif direction == "0":
                self.pan_cam2.setVoltage(0)

    def tilt_move_gen(self, direction):
        if self.game_pad_cam1.get():
            voltage = float(self.tilt_speed_cam1.get())
            if self.invert_tilt_cam1.get():
                voltage *= -1
            if direction == "+":
                self.tilt_cam1.setVoltage(voltage)
            elif direction == "-":
                self.tilt_cam1.setVoltage(-1 * voltage)
            elif direction == "0":
                self.tilt_cam1.setVoltage(0)

        if self.game_pad_cam2.get():
            voltage = float(self.tilt_speed_cam2.get())
            if self.invert_tilt_cam1.get():
                voltage *= -1
            if direction == "+":
                self.tilt_cam2.setVoltage(voltage)
            elif direction == "-":
                self.tilt_cam2.setVoltage(-1 * voltage)
            elif direction == "0":
                self.tilt_cam2.setVoltage(0)


root = Tk()
TIMC = MainWindow(root, SetupMainWindow())
root.mainloop()
print('Clean Exit')
