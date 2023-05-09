# -*- coding: utf-8 -*-

"""
Title: Graphical User Interface to control the Arduino based electrical stimulator
Date of Creation: Fri Sep 11 17:23:16 2020
Author: Themis Efthimiou
"""

##################################################################################################################################

# Find port address for Mac OS:
# to find the address of the serial port, open terminal, and type: ls /dev/* it should be something like: /dev/cu.usbmodem146301

# Find port address for Windows:
# to find the address of the serial port, open device manager, and look under Ports (COM & LPT) it should be something like: COM3
##################################################################################################################################

# Import modules

from tkinter import *

import time

import serial

##################################################################################################################################

# Define Serial
# wake up DACs

ser1 = serial.Serial("/dev/tty.usbmodem1464101",
                     19200, timeout=0, writeTimeout=0)

time.sleep(2)  # wait 2 s

ser1.write(b'\xFF')  # Start device

ser2 = serial.Serial("/dev/tty.usbmodem1464201",
                     19200, timeout=0, writeTimeout=0)

time.sleep(2)  # wait 2 s

ser2.write(b'\xFF')  # Start device

##################################################################################################################################

# Create GUI Window

window = Tk()


window.title("Arduino Controller")

window.geometry()

##################################################################################################################################

# # Click Settings (On, Off, Blink, LED on/off, and Query data), Reset Pulse Count and Start Stim##

# Blink LED


def blink():

    ser.write(b'\x63')  # Send byte for Blink


Blink = Button(window, text="Blink", bg="white", fg="black", width=22,
               height=2, justify='center', wraplength=120, command=blink)

Blink.grid(column=1, row=0)


# Turn Display on or off

def LEDOFF():

    ser1.write(b'\x44')  # Display Off

    ser1.write(b'\x00')

    ser2.write(b'\x44')  # Display Off

    ser2.write(b'\x00')


LED_OFF = Button(window, text="Screen Off", bg="white", fg="black",
                 width=22, height=2, justify='center', wraplength=120, command=LEDOFF)

LED_OFF.grid(column=0, row=1)


def LEDON():

    ser1.write(b'\x45')  # Display On

    ser1.write(b'\x01')

    ser2.write(b'\x45')  # Display On

    ser2.write(b'\x01')


LED_ON = Button(window, text="Screen On", bg="white", fg="black",
                width=22, height=2, justify='center', wraplength=120, command=LEDON)

LED_ON.grid(column=1, row=1)


# ## Query Data

# def Q_Data():

#     ser1.write(b'\x41')
#     ser2.write(b'\x41')


# Query_Data = Button(window, text="Query Data", bg="white", fg="black",width=22, height=2,justify='center',wraplength=120,command=Q_Data)

# Query_Data.grid(column=2, row=1)


# Set Train Count to 0

def Train_Reset():

    ser1.write(b'\x4E')
    ser2.write(b'\x4E')


Set_Count_0 = Button(window, text="Reset Count", bg="white", fg="black", width=22,
                     height=2, justify='center', font="bold", wraplength=120, command=Train_Reset)

Set_Count_0.grid(column=0, row=10)


# Start Stimulation DAC1

def Start_stim_DAC1():

    ser1.write(b'\x50')


def Start_stim_DAC2():

    ser2.write(b'\x50')


def Start_stim_DAC1_2():

    ser1.write(b'\x50')
    ser2.write(b'\x50')


Send_settings = Button(window, text="Start DAC1", bg="green", fg="black",
                       font="bold", width=22, height=2, command=Start_stim_DAC1)

Send_settings.grid(column=1, row=12)

Send_settings = Button(window, text="Start DAC2", bg="green", fg="black",
                       font="bold", width=22, height=2, command=Start_stim_DAC2)

Send_settings.grid(column=2, row=12)

Send_settings = Button(window, text="Start DACS", bg="green", fg="black",
                       font="bold", width=22, height=2, command=Start_stim_DAC1_2)

Send_settings.grid(column=3, row=12)

#   Emergency Stop which interupts the train of pulses


def stop():

    ser1.write(b'\x21')
    ser2.write(b'\x21')


Stop_Train = Button(window, text="STOP", bg="red", fg="black",
                    font="bold", width=22, height=2, command=stop)

Stop_Train.grid(column=0, row=12)


# Close Port

def Close_COM():

    ser1.close()  # Close Port
    ser2.close()  # Close Port


Close_Port = Button(window, text="Close Port", bg="white", fg="black",
                    width=22, height=2, justify='center', wraplength=120, command=Close_COM)

Close_Port.grid(column=0, row=0)

##################################################################################################################################

## Set Pulse Mode: Monopolar (OpAmp Enabled), Monopolar (OpAmp Disabled), Bipolar (OpAmb Enabled)##


def Bipolar():

    ser1.write(b'\x62')  # Set bipolar (OpAmp Enabled)
    ser2.write(b'\x62')  # Set bipolar (OpAmp Enabled)


Bipolar_En = Button(window, text="Bipolar (OpAmp Enabled)", bg="white", fg="black",
                    width=22, height=2, justify='center', wraplength=120, command=Bipolar)

Bipolar_En.grid(column=3, row=3)


def MonopolarEN():

    ser1.write(b'\x61')  # Set Monopolar (OpAmp Enabled)
    ser2.write(b'\x61')  # Set Monopolar (OpAmp Enabled)


Mono_EN = Button(window, text="Monopolar (OpAmp Enabled)", bg="white", fg="black",
                 width=22, height=2, justify='center', wraplength=120, command=MonopolarEN)

Mono_EN.grid(column=3, row=5)

##################################################################################################################################

# Set Trigger mode (0-3)## DAC1


def Trigger_DAC1():

    Trigger1 = int(Trigger_Input1.get())  # Get user input and convert to int

    # Convert integer to byte
    Trig1 = (Trigger1).to_bytes(1, byteorder="little")

    ser1.write(b'\x5A')  # Set Trigger Mode

    ser1.write(Trig1)  # Set Trigger Mode (Available inputs: 0,1,2,3)


Trigger_Message = Label(window, text="Trigger Number", bg="white",
                        fg="black", justify='center', wraplength=120, width=22, height=2)

Trigger_Message.grid(column=0, row=3)


Trigger_Input1 = Entry(window, bg="white", fg="black",
                       font="bold", justify='center')

Trigger_Input1.insert(0, "0")

Trigger_Input1.grid(column=1, row=3)


##################################################################################################################################

# Set Trigger mode (0-3)## DAC2

def Trigger_DAC2():

    Trigger2 = int(Trigger_Input2.get())  # Get user input and convert to int

    # Convert integer to byte
    Trig2 = (Trigger2).to_bytes(1, byteorder="little")

    ser2.write(b'\x5A')  # Set Trigger Mode

    ser2.write(Trig2)  # Set Trigger Mode (Available inputs: 0,1,2,3)


Trigger_Message = Label(window, text="Trigger Number", bg="white",
                        fg="black", justify='center', wraplength=120, width=22, height=2)

Trigger_Message.grid(column=0, row=3)


Trigger_Input2 = Entry(window, bg="white", fg="black",
                       font="bold", justify='center')

Trigger_Input2.insert(0, "0")

Trigger_Input2.grid(column=2, row=3)

##################################################################################################################################

# Labels for GUI

Set_Message = Label(window, text="Settings", bg="white", fg="black",
                    width=22, height=2, justify='center', wraplength=120)

Set_Message.grid(column=0, row=2)


Input_User_Message = Label(window, text="DAC 1 Values", bg="white",
                           fg="black", width=22, height=2, justify='center', wraplength=120)

Input_User_Message.grid(column=1, row=2)

Input_User_Message = Label(window, text="DAC 2 Values", bg="white",
                           fg="black", width=22, height=2, justify='center', wraplength=120)

Input_User_Message.grid(column=2, row=2)

##################################################################################################################################

# Set number of pulses for DAC1


def Pulses_DAC1():

    Pulse_no = int(P_Input.get())  # Get user input and convert to int

    #   Create integer for high & low byte

    # Integer (floor division) divided by high byte for 'Pulse Repetition Time' (256)
    HB_p = Pulse_no//256

    LB_p = int((Pulse_no % 256)/1)  # Calculate remainder (modulo division)

    #   Create high and low byte for serial command

    P_HB = (HB_p).to_bytes(1, byteorder="little")  # Convert integer to byte

    P_LB = (LB_p).to_bytes(1, byteorder="little")  # Convert integer to byte

    #   Send Serial Command for Repetition Time

    ser1.write(b'\x59')  # Send serial Command to input number of pulses (x59)

    ser1.write(P_HB)  # Set Highbyte

    ser1.write(P_LB)  # Set Lowbyte


P_Message = Label(window, text="Number of Pulses (1-9999)", bg="white",
                  fg="black", width=22, height=2, justify='center', wraplength=120)

P_Message.grid(column=0, row=4)

P_Input = Entry(window, bg="white", fg="black", justify='center', font="bold")

P_Input.insert(0, "30")

P_Input.grid(column=1, row=4)

##################################################################################################################################

# Set number of pulses for DAC2


def Pulses_DAC2():

    Pulse_no = int(P_Input2.get())  # Get user input and convert to int

    #   Create integer for high & low byte

    # Integer (floor division) divided by high byte for 'Pulse Repetition Time' (256)
    HB_p = Pulse_no//256

    LB_p = int((Pulse_no % 256)/1)  # Calculate remainder (modulo division)

    #   Create high and low byte for serial command

    P_HB = (HB_p).to_bytes(1, byteorder="little")  # Convert integer to byte

    P_LB = (LB_p).to_bytes(1, byteorder="little")  # Convert integer to byte

    #   Send Serial Command for Repetition Time

    ser2.write(b'\x59')  # Send serial Command to input number of pulses (x59)

    ser2.write(P_HB)  # Set Highbyte

    ser2.write(P_LB)  # Set Lowbyte


P_Message = Label(window, text="Number of Pulses (1-9999)", bg="white",
                  fg="black", width=22, height=2, justify='center', wraplength=120)

P_Message.grid(column=0, row=4)

P_Input2 = Entry(window, bg="white", fg="black", justify='center', font="bold")

P_Input2.insert(0, "30")

P_Input2.grid(column=2, row=4)

##################################################################################################################################

# Set Ouput Voltage Width - DAC1


def Output_Voltage_DAC1():

    OV = float(OV_Input.get())  # Get user input


#   Create integer for high and low byte

    # Input (floor division) divided by high byte for 'Output Voltage' (128 mV) and convert to int
    HB_ov = int(OV//128)

    # Calculate remainder (modulo division), then divide by low byte (0.5)) and convert to int
    LB_ov = int((OV % 128)/0.5)


#   Covert int to byte for high and low byte for serial command

    OV_HB = (HB_ov).to_bytes(1, byteorder="little")  # Convert integer to byte

    OV_LB = (LB_ov).to_bytes(1, byteorder="little")  # Convert integer to byte


#   Send Serial Command for voltage output (x53)

    ser1.write(b'\x53')  # Serial Command for Repetition Time

    ser1.write(OV_HB)  # Set Highbyte

    ser1.write(OV_LB)  # Set Lowbyte

#   Create high and low byte for serial command


OV_Message = Label(window, text="Output Voltage (mV)", bg="white",
                   fg="black", width=22, height=2, justify='center', wraplength=120)

OV_Message.grid(column=0, row=9)


OV_Input = Entry(window, bg="white", fg="black", font="bold", justify='center')

OV_Input.insert(0, "0")

OV_Input.grid(column=1, row=9)

##################################################################################################################################


# Set Ouput Voltage Width - DAC2

def Output_Voltage_DAC2():

    OV = float(OV_Input2.get())  # Get user input


#   Create integer for high and low byte

    # Input (floor division) divided by high byte for 'Output Voltage' (128 mV) and convert to int
    HB_ov = int(OV//128)

    # Calculate remainder (modulo division), then divide by low byte (0.5)) and convert to int
    LB_ov = int((OV % 128)/0.5)


#   Covert int to byte for high and low byte for serial command

    OV_HB = (HB_ov).to_bytes(1, byteorder="little")  # Convert integer to byte

    OV_LB = (LB_ov).to_bytes(1, byteorder="little")  # Convert integer to byte


#   Send Serial Command for voltage output (x53)

    ser2.write(b'\x53')  # Serial Command for Repetition Time

    ser2.write(OV_HB)  # Set Highbyte

    ser2.write(OV_LB)  # Set Lowbyte

#   Create high and low byte for serial command


OV_Message = Label(window, text="Output Voltage (mV)", bg="white",
                   fg="black", width=22, height=2, justify='center', wraplength=120)

OV_Message.grid(column=0, row=9)


OV_Input2 = Entry(window, bg="white", fg="black",
                  font="bold", justify='center')

OV_Input2.insert(0, "0")

OV_Input2.grid(column=2, row=9)

##################################################################################################################################
# Delay in-between pulses of a train (milliseconds) DAC1


def Pulse_Delay_ms_DAC1():

    PD_ms = int(PP_Input.get())  # Get user input and conv to byte


#   Create integer for highbyte and lowbyte

    # Integer (floor division) divided by high byte for high byte (26.6 ms)
    PDms_hb = int(PD_ms//25.6)

    # Input divide (modulo division) low byte (0.1) then conv to int
    PDms_lb = int(round(((PD_ms % 25.6)/.1), 2))


#   Create high and low byte for serial command

    PDms_HB = (PDms_hb).to_bytes(
        1, byteorder="little")  # Convert integer to byte

    PDms_LB = (PDms_lb).to_bytes(
        1, byteorder="little")  # Convert integer to byte


#   Send Serial Command for Pulse Width in microseconds (x58) if input is > 0

    if (PDms_hb > 0 or PDms_lb > 0):

        #   Send Serial Command for Repetition Time

        ser1.write(b'\x58')  # Serial Command for Repetition Period

        ser1.write(PDms_HB)  # Set Highbyte

        ser1.write(PDms_LB)  # Set Lowbyte


PP_Message = Label(window, text="Pulse Delay (ms)", bg="white",
                   fg="black", width=22, height=2, justify='center', wraplength=120)

PP_Message.grid(column=0, row=5)


PP_Input = Entry(window, bg="white", fg="black",
                 width=20, font="bold", justify='center')

PP_Input.insert(0, "17")

PP_Input.grid(column=1, row=5)

##################################################################################################################################

# Delay in-between pulses of a train (milliseconds) DAC2


def Pulse_Delay_ms_DAC2():

    PD_ms = int(PP_Input2.get())  # Get user input and conv to byte


#   Create integer for highbyte and lowbyte

    # Integer (floor division) divided by high byte for high byte (26.6 ms)
    PDms_hb = int(PD_ms//25.6)

    # Input divide (modulo division) low byte (0.1) then conv to int
    PDms_lb = int(round(((PD_ms % 25.6)/.1), 2))


#   Create high and low byte for serial command

    PDms_HB = (PDms_hb).to_bytes(
        1, byteorder="little")  # Convert integer to byte

    PDms_LB = (PDms_lb).to_bytes(
        1, byteorder="little")  # Convert integer to byte


#   Send Serial Command for Pulse Width in microseconds (x58) if input is > 0

    if (PDms_hb > 0 or PDms_lb > 0):

        #   Send Serial Command for Repetition Time

        ser2.write(b'\x58')  # Serial Command for Repetition Period

        ser2.write(PDms_HB)  # Set Highbyte

        ser2.write(PDms_LB)  # Set Lowbyte


PP_Message = Label(window, text="Pulse Delay (ms)", bg="white",
                   fg="black", width=22, height=2, justify='center', wraplength=120)

PP_Message.grid(column=0, row=5)


PP_Input2 = Entry(window, bg="white", fg="black",
                  width=20, font="bold", justify='center')

PP_Input2.insert(0, "17")

PP_Input2.grid(column=2, row=5)

##################################################################################################################################
# Delay in-between pulses of a train (microseconds) DAC1


def Pulse_Delay_us_DAC1():

    PD_us = int(PDus_Input.get())  # Get user input and conv to byte


#   Create integer for highbyte and lowbyte

    # Integer (floor division) divided by high byte for high byte (26.6 ms)
    PDus_hb = PD_us//256

    # Input divide (modulo division) low byte (0.1) then conv to int
    PDus_lb = int((PD_us % 256)/1)


#   Create high and low byte for serial command

    PDus_HB = (PDus_hb).to_bytes(
        1, byteorder="little")  # Convert integer to byte

    PDus_LB = (PDus_lb).to_bytes(
        1, byteorder="little")  # Convert integer to byte


#   Send Serial Command for Pulse Width in microseconds (x3A) if input is > 0

    if (PDus_hb > 0 or PDus_lb > 0):

        #   Send Serial Command for Repetition Time

        ser1.write(b'\x3A')  # Serial Command for Repetition Period

        ser1.write(PDus_HB)  # Set Highbyte

        ser1.write(PDus_LB)  # Set Lowbyte


PDus_Message = Label(window, text="Pulse Delay (us)", bg="white",
                     fg="black", width=22, height=2, justify='center', wraplength=120)

PDus_Message.grid(column=0, row=6)


PDus_Input = Entry(window, bg="white", fg="black",
                   width=20, font="bold", justify='center')

PDus_Input.insert(0, "0")

PDus_Input.grid(column=1, row=6)

##################################################################################################################################

# Delay in-between pulses of a train (microseconds) DAC2


def Pulse_Delay_us_DAC2():

    PD_us = int(PDus_Input2.get())  # Get user input and conv to byte


#   Create integer for highbyte and lowbyte

    # Integer (floor division) divided by high byte for high byte (26.6 ms)
    PDus_hb = PD_us//256

    # Input divide (modulo division) low byte (0.1) then conv to int
    PDus_lb = int((PD_us % 256)/1)


#   Create high and low byte for serial command

    PDus_HB = (PDus_hb).to_bytes(
        1, byteorder="little")  # Convert integer to byte

    PDus_LB = (PDus_lb).to_bytes(
        1, byteorder="little")  # Convert integer to byte


#   Send Serial Command for Pulse Width in microseconds (x3A) if input is > 0

    if (PDus_hb > 0 or PDus_lb > 0):

        #   Send Serial Command for Repetition Time

        ser2.write(b'\x3A')  # Serial Command for Repetition Period

        ser2.write(PDus_HB)  # Set Highbyte

        ser2.write(PDus_LB)  # Set Lowbyte


PDus_Message = Label(window, text="Pulse Delay (us)", bg="white",
                     fg="black", width=22, height=2, justify='center', wraplength=120)

PDus_Message.grid(column=0, row=6)


PDus_Input2 = Entry(window, bg="white", fg="black",
                    width=20, font="bold", justify='center')

PDus_Input2.insert(0, "0")

PDus_Input2.grid(column=2, row=6)

##################################################################################################################################

# Set Pulse Width (milliseconds) DAC1


def Pulse_Width_ms_DAC1():

    PW_ms = int(PWms_Input.get())  # Get user input


#   Create integer for highbyte

    # Integer (floor division) divided by high byte for pulse width (25.6 ms)
    PWms_hb = int(PW_ms//25.6)

    # Take user input modulo division by 25.6 and divide by 0.1 then convert to int
    PWms_lb = int(round(((PW_ms % 25.6)/.1), 2))


#   Create high and low byte for serial command

    PWms_HB = (PWms_hb).to_bytes(
        1, byteorder="little")  # Convert integer to byte

    PWms_LB = (PWms_lb).to_bytes(
        1, byteorder="little")  # Convert integer to byte


#   Send Serial Command for Repetition Time (x57)

    if PWms_hb > 0 or PWms_lb > 0:

        ser1.write(b'\x57')  # Serial Command for Pulse Width

        ser1.write(PWms_HB)  # Set Highbyte

        ser1.write(PWms_LB)  # Set Lowbyte


PWms_Message = Label(window, text="Pulse Width (ms)", bg="white",
                     fg="black", width=22, height=2, justify='center', wraplength=120)

PWms_Message.grid(column=0, row=7)


PWms_Input = Entry(window, bg="white", fg="black",
                   font="bold", justify='center')

PWms_Input.insert(0, "0")

PWms_Input.grid(column=1, row=7)

##################################################################################################################################

# Set Pulse Width (milliseconds) DAC2


def Pulse_Width_ms_DAC2():

    PW_ms = int(PWms_Input2.get())  # Get user input


#   Create integer for highbyte

    # Integer (floor division) divided by high byte for pulse width (25.6 ms)
    PWms_hb = int(PW_ms//25.6)

    # Take user input modulo division by 25.6 and divide by 0.1 then convert to int
    PWms_lb = int(round(((PW_ms % 25.6)/.1), 2))


#   Create high and low byte for serial command

    PWms_HB = (PWms_hb).to_bytes(
        1, byteorder="little")  # Convert integer to byte

    PWms_LB = (PWms_lb).to_bytes(
        1, byteorder="little")  # Convert integer to byte


#   Send Serial Command for Repetition Time (x57)

    if PWms_hb > 0 or PWms_lb > 0:

        ser2.write(b'\x57')  # Serial Command for Pulse Width

        ser2.write(PWms_HB)  # Set Highbyte

        ser2.write(PWms_LB)  # Set Lowbyte


PWms_Message = Label(window, text="Pulse Width (ms)", bg="white",
                     fg="black", width=22, height=2, justify='center', wraplength=120)

PWms_Message.grid(column=0, row=7)


PWms_Input2 = Entry(window, bg="white", fg="black",
                    font="bold", justify='center')

PWms_Input2.insert(0, "0")

PWms_Input2.grid(column=2, row=7)

##################################################################################################################################
# Set Pulse Width (milliseconds) DAC1


def Pulse_Width_us_DAC1():

    PW_us = int(PWus_Input2.get())  # Get user input


#   Create integer for highbyte

    # Integer (floor division) divided by high byte for repeition width (256 ms)
    PWus_hb = PW_us//256

    # Take user input modulo division by 25.6 and divide by 1 then convert to int
    PWus_lb = int((PW_us % 256)/1)


#   Create high and low byte for serial command

    PWus_HB = (PWus_hb).to_bytes(
        1, byteorder="little")  # Convert integer to byte

    PWus_LB = (PWus_lb).to_bytes(
        1, byteorder="little")  # Convert integer to byte


#   Send Serial Command for Repetition Time (39)

    if PWus_hb > 0 or PWus_lb > 0:

        ser1.write(b'\x39')  # Serial Command for Pulse Width

        ser1.write(PWus_HB)  # Set Highbyte

        ser1.write(PWus_LB)  # Set Lowbyte


PWus_Message = Label(window, text="Pulse Width (μs)", bg="white",
                     fg="black", width=22, height=2, justify='center', wraplength=120)

PWus_Message.grid(column=0, row=8)


PWus_Input2 = Entry(window, bg="white", fg="black",
                    font="bold", justify='center')

PWus_Input2.insert(0, "100")

PWus_Input2.grid(column=1, row=8)

##################################################################################################################################

# Set Pulse Width (milliseconds) DAC2


def Pulse_Width_us_DAC2():

    PW_us = int(PWus_Input2.get())  # Get user input


#   Create integer for highbyte

    # Integer (floor division) divided by high byte for repeition width (256 ms)
    PWus_hb = PW_us//256

    # Take user input modulo division by 25.6 and divide by 1 then convert to int
    PWus_lb = int((PW_us % 256)/1)


#   Create high and low byte for serial command

    PWus_HB = (PWus_hb).to_bytes(
        1, byteorder="little")  # Convert integer to byte

    PWus_LB = (PWus_lb).to_bytes(
        1, byteorder="little")  # Convert integer to byte


#   Send Serial Command for Repetition Time (39)

    if PWus_hb > 0 or PWus_lb > 0:
        ser2.write(b'\x39')  # Serial Command for Pulse Width

        ser2.write(PWus_HB)  # Set Highbyte

        ser2.write(PWus_LB)  # Set Lowbyte


PWus_Message = Label(window, text="Pulse Width (μs)", bg="white",
                     fg="black", width=22, height=2, justify='center', wraplength=120)

PWus_Message.grid(column=0, row=8)


PWus_Input2 = Entry(window, bg="white", fg="black",
                    font="bold", justify='center')

PWus_Input2.insert(0, "100")

PWus_Input2.grid(column=2, row=8)

##################################################################################################################################
# Set parameters for DAC1


def Send():

    Trigger_DAC1()

    Pulses_DAC1()

    Pulse_Delay_ms_DAC1()

    Pulse_Delay_us_DAC1()

    Pulse_Width_ms_DAC1()

    Pulse_Width_us_DAC1()

    Output_Voltage_DAC1()


Send_settings = Button(window, text="Set DAC1", bg="white",
                       fg="black", font="bold", width=22, height=2, command=Send)

Send_settings.grid(column=1, row=10)

##################################################################################################################################

##################################################################################################################################
# Set parameters for DAC2


def Send():

    Trigger_DAC2()

    Pulses_DAC2()

    Pulse_Delay_ms_DAC2()

    Pulse_Delay_us_DAC2()

    Pulse_Width_ms_DAC2()

    Pulse_Width_us_DAC2()

    Output_Voltage_DAC2()


Send_settings = Button(window, text="Set DAC2", bg="white",
                       fg="black", font="bold", width=22, height=2, command=Send)

Send_settings.grid(column=2, row=10)

##################################################################################################################################

##################################################################################################################################
# Send commands to both DACS


def Send_DACS():

    Trigger_DAC1()

    Pulses_DAC1()

    Pulse_Delay_ms_DAC1()

    Pulse_Delay_us_DAC1()

    Pulse_Width_ms_DAC1()

    Pulse_Width_us_DAC1()

    Output_Voltage_DAC1()

    Trigger_DAC2()

    Pulses_DAC2()

    Pulse_Delay_ms_DAC2()

    Pulse_Delay_us_DAC2()

    Pulse_Width_ms_DAC2()

    Pulse_Width_us_DAC2()

    Output_Voltage_DAC2()


Send_settings = Button(window, text="Set DAC1 & DAC2", bg="white",
                       fg="black", font="bold", width=22, height=2, command=Send_DACS)

Send_settings.grid(column=3, row=10)

##################################################################################################################################
# Loop window

window.mainloop()
