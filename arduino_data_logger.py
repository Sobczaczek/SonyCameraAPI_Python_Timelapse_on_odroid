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
import os

saveFilePath = '/media/odroid/KINGSTON/sony_timelapse'
# SAVE
def saveStatus(s):
    # open file in append mode
    while not os.path.exists(saveFilePath):
        # stay until path is found (example: pendrive mounted)
        print("Waiting")

    log = open(saveFilePath+'/datalog.txt', 'a')
    separator = "----------------------------------------------------------------------------------------------------\n"
    # log separatos
    log.write(separator)
    # save text
    log.write(s)
    # close file
    log.close()
    
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
buffer = ""
tempINcmd = b'[OP_GET|TEMPERATURE_IN]'
humdINcmd = b'[OP_GET|HUMIDITY_IN]'
dewINcmd = b'[OP_GET|DEWPOINT_IN]'

tempOUTcmd = b'[OP_GET|TEMPERATURE_OUT]'
humdOUTcmd = b'[OP_GET|HUMIDITY_OUT]'
dewOUTcmd = b'[OP_GET|DEWPOINT_OUT]'

while True:
    startTime = time.time()
    buffer = str(datetime.fromtimestamp(int(time.time())))
    # get temp inside
    arduino.write(tempINcmd)
    time.sleep(0.4)
    buffer+=str(arduino.read_until(expected=']'))

    arduino.write(humdINcmd)
    time.sleep(0.4)
    buffer+=str(arduino.read_until(expected=']'))

    arduino.write(dewINcmd)
    time.sleep(0.4)
    buffer+=str(arduino.read_until(expected=']'))

    arduino.write(tempOUTcmd)
    time.sleep(0.4)
    buffer+=str(arduino.read_until(expected=']'))

    arduino.write(humdOUTcmd)
    time.sleep(0.4)
    buffer+=str(arduino.read_until(expected=']'))

    arduino.write(dewOUTcmd)
    time.sleep(0.4)
    buffer+=str(arduino.read_until(expected=']'))

    # save file
    saveStatus(buffer)

    print(buffer)
    time.sleep(600.0 - ((time.time() - startTime) % 600))
    
# get temp outside
