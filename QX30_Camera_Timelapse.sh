#!/bin/bash -x
#@brief 	Shell script for SONY CAMERA TIMELAPSE
#@author	Dawid Sobczak
#@date 		23-05-2022
#@version	1.3

#HARDWARE
# ODROID XU3
# SONY DSC-QX30 Camera

#STEP 0. PREPARATION ----------------------------------------------------------------------------
# Force device power on using GPIO Output as trigger switch.
# Used GPIO pin: 
#	Linux notation -> #GPIO21
#	Physical -> PIN 13

#STEP 1. WIFI CONNECTION ------------------------------------------------------------------------
# Force ODROID to make connection with SONY Camera WiFi.
# If connection is established -> Continue to STEP [2]
# Else repeat STEP [1]
# Additional condition -> is conection could not be established more than x times -> force device power on again

#STEP 2. API CONNECTION -------------------------------------------------------------------------
# Search available camera, authenticate it and run timelapse script


#STEP [0] =======================================================================================
sleep 20
#. cd /home/odroid/Timelapse_budowa/
# export GPIO 21 from GPIO Class
echo 21 >/sys/class/gpio/export
sleep 5
# save and check export state
CHECK0=$(echo $?)

# set exported GPIO as a OUTPUT
echo out >/sys/class/gpio/gpio21/direction
sleep 5
# force HIGH state for 3 seconds, return to LOW
##echo 1 >/sys/class/gpio/gpio21/value && sleep 3 && echo 0 >/sys/class/gpio/gpio21/value
sleep 5
#STEP [1] =======================================================================================
# variables -------------------------------------------------------------------------------------

# Sony camera wifi SSID and Password (can be changed for specific camera)
CAMERA_SSID="DIRECT-bBQ1:DSC-QX30"
CAMERA_PASSWD="JCVWrK2A"

# State checks
# CHECK0 -
# CHECK1 -
# CHECK2 -
# CHECK3 -

# Iterators
ITERATOR1=0

# end variables ---------------------------------------------------------------------------------

# Wifi connection forced in shell script -------------------------------------------------------- 
# nmcli connect ->	 no network with given SSID found ->	 status code: 10
# nmcli connect -> 	 succesfully activated     	  -> 	 status code: 0

# Force WIFI connection
nmcli d wifi connect $CAMERA_SSID password $CAMERA_PASSWD 

# Save WIFI connection state
CHECK1=$(echo $?)

# Check if connection is established
while [ $CHECK1 -ne 0 ]
do
	echo 'bash: Could not establish wifi connection with:'
	echo $CAMERA_SSID
	# wait some time
	echo 'Sleeping...'
	sleep 10
	# try to connect again, and save state
	nmcli d wifi connect $CAMERA_SSID password $CAMERA_PASSWD
	CHECK1=$(echo $?)
	# incrementation
	ITERATOR1=$(($ITERATOR1+1))
	# check iteration
	if [ $ITERATOR1 -eq 8 ]
	then
		# force HIGH state for 3 seconds, return to LOW
		echo 1 >/sys/class/gpio/gpio21/value && sleep 3 && echo 0 >/sys/class/gpio/gpio21/value
		ITERATOR1=0
	fi
done
echo 'bash: WIFI connection established'
# create wifi route
sleep 5
route > /tmp/przed_routem.txt 2> /tmp/przed_routem2.txt
ifconfig >> /tmp/przed_routem.txt

/sbin/route add -net 239.255.255.250/31 wlan0 > /tmp/routelog.txt 2> /tmp/routelog2.txt

echo "-----------" >> /tmp/przed_routem.txt
echo "-----------" >> /tmp/przed_routem2.txt

route >> /tmp/przed_routem.txt
ifconfig >> /tmp/przed_routem.txt
#ip route add 239.255.255.250/31 dev wlan0 

#STEP [2] =======================================================================================
# run virtualenv (is it necceseary?)
#cd /home/odroid/TIMELAPSE/sony_camera
#source bin/activate
#cd /home/odroid/TIMELAPSE/sony_camera/sony_camera_api/timelapse

# run logger 
/usr/bin/python3 /home/odroid/Timelapse_budowa/arduino_data_logger.py &
# run script (), check output
/usr/bin/python3 /home/odroid/Timelapse_budowa/QX30_Camera_Timelapse.py
CHECK2=$(echo $?)
while [ $CHECK2 -eq 2 ]
do
    sleep 5
    /usr/bin/python3 /home/odroid/Timelapse_budowa/QX30_Camera_Timelapse.py
    CHECK2=$(echo $?)
done

# end
