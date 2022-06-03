# @autor Dawid Sobczak
# @date 2022-06-03
# @brief Arduino serial port communication protocole
#
# Tested on:
# Arduino Micro

# IMPORTS ==============================================================================================================
import serial
import time
import json
from datetime import datetime
import sys

# SERIAL PORT ==========================================================================================================
# open serial port
arduino = serial.Serial('/dev/serial/by-id/usb-Arduino_LLC_Arduino_Micro-if00', 9600,
                        timeout=1, parity=serial.PARITY_NONE)

# print serial name to check
print(arduino.name)

# ping device
arduino.write(b'[OP_GET|PING]')
time.sleep(0.4)
text = arduino.read_until(expected=']')
time.sleep(1)

print(text)

# read data
tempIN = 0
tempOUT = 0
humdIN = 0
humdOUT = 0
dewPointIN = 0
dewPointOUT = 0
buffer = [[]]
tempINcmd = b'[OP_GET|TEMPERATURE_IN]'
humdINcmd = b'[OP_GET|HUMIDITY_IN]'
dewINcmd = b'[OP_GET|DEWPOINT_IN]'

tempOUTcmd = b'[OP_GET|TEMPERATURE_OUT]'
humdOUTcmd = b'[OP_GET|HUMIDITY_OUT]'
dewOUTcmd = b'[OP_GET|DEWPOINT_OUT]'


def main(args):
    print(datetime.fromtimestamp(int(time.time())))
    for arg in args:
        if arg == "tempIN":
            arduino.write(tempINcmd)
            time.sleep(0.4)
            print(arduino.read_until(expected=']'))
        elif arg == 'tempOUT':
            arduino.write(tempOUTcmd)
            time.sleep(0.4)
            print(arduino.read_until(expected=']'))
        elif arg =='humdIN':
            arduino.write(humdINcmd)
            time.sleep(0.4)
            print(arduino.read_until(expected=']'))
        elif arg =='humdOUT':
            arduino.write(humdOUTcmd)
            time.sleep(0.4)
            print(arduino.read_until(expected=']'))
        elif arg =='dewIN':
            arduino.write(dewINcmd)
            time.sleep(0.4)
            print(arduino.read_until(expected=']'))
        elif arg =='dewOUT':
            arduino.write(dewOUTcmd)
            time.sleep(0.4)
            print(arduino.read_until(expected=']'))
        elif arg == "arduino_communication.py":
            #NOTHING
            print("~ARDUINO SERIAL COMMUNICATION~")
        else:
            print('Wrong or none argument!')


if __name__ == '__main__':
    main(sys.argv)
