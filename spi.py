#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import glob
import time
 

def calculate_temp(raw):
    """Accepts raw output of DS18b20 sensor and returns a tuple of temp in C and F.
    """
    equals_pos = raw[1].find('t=')
    if equals_pos != -1:
        temp_string = raw[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return (temp_c, temp_f)


base_dir = '/sys/bus/w1/devices/'
# Find all the devices that match the signature '28'
temperature_devices = glob.glob(base_dir + '28*')

# isolate the names of the individual devices
device_list = []
for device in temperature_devices:
    device_list.append(device)


def read_temp():
    """Poll each of the devices found and build a list of data.
    """
    measurements = []
    for i, device in enumerate(device_list):
        # add the sub-directory name that holds the temperature data
        d = Path(device, 'w1_slave')
        # open the file as readonly
        file_handle = open(d, 'r')
        # gather the data
        lines = file_handle.readlines()
        file_handle.close()
        temps = calculate_temp(lines)
        # build the result output for this device
        celcius, farenheiht = temps
        out = [f"Device:{i} ID# {Path(device).name} , {celcius:.2f}C {farenheiht:.1f}F"]
        measurements.append(out)
    return measurements


while True:
	print(read_temp())	
	time.sleep(1)