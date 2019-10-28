import time
import serial
import random
import numpy as np
import matplotlib.pyplot as plt

#print('please input the name of the port that the printer is connected to (e.g. COM3)')
com = "COM4"

if 'ser' in globals() and ser.isOpen() == False: ## checks if ser is defined already and if connection is open
    ## configures the serial connection:
    ser = serial.Serial(
        port = com,
        baudrate=38400,
    )
elif 'ser' in globals() and ser.isOpen() == True:
    ser.flushInput()
    ser.flushOutput()
else:
    ser = serial.Serial(
        port = com,
        baudrate=38400,
    )

ser.write(b'\r\n\r\n')
time.sleep(2)
ser.flushInput()

ser.write(b'M42 P9 S255\r\n')       # turns on RAMPS fan
ser.write(b'M42 P4 S255\r\n')       # turns on horizontal extruder fan
ser.write(b'M106 S100\r\n')         # turns on small nozzle fan

# generate random values

F_list = []
E_list = []

#F_list.extend(str(random.randint(100,3000)) for i in range(1))
#E_list.extend(str(random.randint(3,40)) for i in range(1))
print(E_list,F_list)

ser.write(b'M140 S20\r\n')          # heats bed to 70C
ser.write(b'M104 S210\r\n') # heats nozzle to 210C
ser.write(b'G92 E0\r\n')
print('bed & nozzle heating up...\n')

# start building

input("wait for heating and press enter to continue")
E_list.append(str(input("E:")))
F_list.append(str(input("F:")))


ser.write(b'G90' +b'\r\n')           # absolute positioning
ser.write(b'G28\r\n')               # go to home position
ser.write(b'G1 F900 E20\r\n')          # starting blob
ser.write(b'G92 E0\r\n')
ser.write(b'G0 F3000 Z0.5' +b'\r\n')
ser.write(b'G0 F3000  X90 Y40' +b'\r\n')   # go to centre
ser.write(b'G91' +b'\r\n')           # relative positioning
#ser.write(b'G1 F900 E15\r\n')
#ser.write(b'G92 E0\r\n')

# loop

ser.reset_input_buffer()
for i in range(20):
    ser.write(b'G1 F' + F_list[0].encode() +b'\r\n')
    ser.readline()
    ser.write(b'G1 X15 E'  + E_list[0].encode() +b'\r\n')
    ser.readline()
    ser.write(b'G1 Y15 E'  + E_list[0].encode() +b'\r\n')
    ser.readline()
    ser.write(b'G1 X-15 E'  + E_list[0].encode() +b'\r\n')
    ser.readline()
    ser.write(b'G1 Y-15 E'  + E_list[0].encode() +b'\r\n')
    ser.readline()
    ser.write(b'G92 E0\r\n')
    ser.readline()
    ser.write(b'G0 Z0.35' +b'\r\n')
    ser.readline()
    time.sleep(1)
ser.write(b'G0 F3000 Z4' +b'\r\n')
ser.close()


