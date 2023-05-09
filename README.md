# fNMES-GUI
This GitHub repository contains a Python script that implements a graphical user interface (GUI) for controlling electrical stimulators using Arduinos. The script allows users to send commands to the Arduinos, providing precise control over various electrical stimulation parameters.

The GUI was programmed using Python 3.8.5 using the tkinter package. You will also need the modules serial (to send serial commands) and time (to initiate a delay in the commands, i.e. time.sleep).  

The Py script requires the location of the Arduino and a BaudRate (19200 should be used, set your device to this). For windows, a ‘COM’ port is required, and for Linux and mac os, it will need a “/dev/ttyACM0” location. To find your port follow:

Mac os & Linux:
1.Open terminal 
2. type: ‘ls /dev/tty*’ note the port number listed for /dev/ttyUSB* or /dev/ttyACM* 
3. The port number is represented with * here.
Windows:
1. Open Device Manager (Start → Control Panel → Hardware and Sound → Device Manager)
2. Look in the Device Manager list, open the category “Ports” and find the matching COM port.
3. Take the number in the bracket behind the port description.

The GUI sends Hex commands to the Arduino to trigger commands in the firmware (DS5 controlled built by Andreas Gartus, 2020). The codes have a decimal and hex identifier
•	If coding in Matlab use the decimal as codes (e.g. to start to use the code ‘99’
•	If coding in Python use the Hex codes without the 0 (e.g. to start to use the code ‘xFF’)
GUI commands are either input (requiring a number) or a button. These are separated going forward and explained:

Click buttons:
The Start button sends the command’ 255 (0xFF): Start device’; this is only required once and will set the Arduino display to default settings. In addition, it opens the port to received serial commands.
The Blink button sends the command ’99 (0x63): Identify device by blinking display’. This will cause the screen to blink. It acts as a test that commands are sending; however, do not use as there it does not turn off. 
The Display Off sends the command ’69 (0x45) + 1: Turn on display’ which turns the Arduino screen off.
The Display On sends the command ’68 (0x44) + 0: Turn off display’ which turns the Arduino screen on.
The command Reset Pulse sends the command ’78 (0x4E): Zero pulse count’ which sets the pulse count to 0.
The command Query Data sends the command ’65 (0x41): Query data’ which tells the Arduino to display the current parameter settings.
The command Set All will send all input parameters (trigger, pulse width, voltage, etc.) to the Arduino.
The button START sends the command ’80 (0x50): Start pulse sequence (triggers and analogue output)’ which starts the pulse sequence.
The button STOP is an emergency button which terminates the pulse sequence. This uses the serial command: ’33 (0x21): Emergency stop pulse sequence.’
The command, Close port will close the port and sending serial commands will no longer work. To re-activate press, Start again. In the situation where it does not work, close GUI and unplug Arduino then re-connect and run the GUI again.
The commands to set the configuration are as follows:
Bipolar OpAmp enabled '98 (0x62): Set pulse mode to bipolar (OpAmp enabled)'
Monopolar OpAmp enabled '97 (0x61): Set pulse mode to monopolar (OpAmp enabled)'
Monopolar OpAmp disabled '96 (0x60): Set pulse mode to monopolar (OpAmp disabled)'

Explanations:
•	“OpAmp enabled or disabled”:
The original controller does not contain an OpAmp (= operational amplifier), which is needed for bipolar stimulation. Therefore, Andreas included a jumper in the new hardware to disable the OpAmp and by this make it work similar like the original. 
•	Monopolar stimulation can be achieved with enabled or disabled OpAmp (but the DAC needs to be controlled in a different way). So, the firmware needs to know whether the OpAmp is enabled or disabled. 
•	You will most likely only use it with enabled OpAmp (which is also the default). [Or in other words: Disabling the OpAmp requires to set a jumper on the hardware and then bipolar stimulation is no longer possible. Even when the controller is set to bipolar stimulation.]

Input Commands
The input commands set the parameters of the stimulation parameters to use either millisecond (ms), microseconds (us), volts (v), microvolts (mV) and integers. Note, the use of high bytes (HB) and low bytes (LB).
These units are used in the Py script calculation. The input from the GUI is a string; this is first converted into an integer. It is then divided by the HB for the unit of measurement; for example, the voltage will be the integer//128. Notice // is used, in Python, this is floor division returning the largest possible integer which is used as the HB. The remainder from the division is then divided by the unit for the LB, using the same example (voltage) it will be remainder/0.5 giving us the LB. Both the HB and LB are converted into bytes and sent with serial command.
Command	Integer	HB	LB
Number of Pulses	1	256	1
Delay in-between pulses (ms)	1	25.6 ms	100 us
Pulse Width (ms)	1	25.6 ms	100 us
Voltage	1	128 mV	0.5 mV
Delay in-between pulses (us)	1	256 us	10 us
Pulse Width (us)	1	256 us	10 us
The input “Enter Trigger Number” works with the command ’90 (0x5A) + Byte: Set trigger mode (T0, T1, T2, T3)’. You should use the numbers 0, 1, 2, 3 (corresponding respectively to T0, T1, T2, T3), anything greater than three will act as T3. 

Explanation:
   T0 = send no trigger
   T1 = send trigger on channel 1
   T2 = send trigger on channel 2
   T3 = send triggers on channel 1 & 2
The input for “Number of Pulses (1-9999)” will set the number of pulses in the pulse train and is a unit-less number. 
The input for “Pulse Repetition Period (ms)” 88 (0x58) + HighByte + LowByte: Set pulse repetition period [1...99999 * 0.1ms]. This sets the delay between each pulse of a train (e.g. if there are ten pulses in a train, this can add a 5us delay between each one).
The input for “Pulse Width (μs)” the pulse width in microseconds sending the command 58 (0x3A) + HighByte + LowByte: Set pulse repetition period [10...9999 * 1us].  This defines the length of a single pulse (see image below).
The input for "Enter Output Voltage" will set the voltage sending them command 83 (0x53) + HighByte + LowByte: Set output voltage [0...4095 * 0.5mV]. The DS5 has a current output, but it is controlled by a voltage sent by the Arduino controller. It depends on the setting of the DS5 how this voltage translates into the current. But the Arduino does not know about this setting; hence you can only set the output voltage. If I remember correctly, you can, e.g. set the DS5 to 1V = 1mA. Thus, if the Arduino would send 0.2V (= 200mV), the DS5 would produce 0.2mA (= 200uA) output.
The image below displays a biphasic pulse, the pulse width defines how long each pulse is active. The monophasic and biphasic pulse differ in an important way, if you for example choose a pulse width of 200 us, a biphasic pulse is positive and negative phase for 100 ms respectively. Whereas the monophasic pulse will be in positive phase for the entire defined period, following our example 200 us.
