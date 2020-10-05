#!/usr/bin/env python
# -*- coding: utf-8 -*-

SPI_DEVICE_PATH = "/sys/bus/w1/devices/"

from pathlib import Path
import glob
import time
from time_strings import UTC_NOW_STRING
from data2csv import write_csv
from loguru import logger


@logger.catch
def calculate_temp(raw):
    """Accepts raw output of DS18b20 sensor and returns a tuple of temp in C and F."""
    equals_pos = raw[1].find("t=")
    if equals_pos != -1:
        temp_string = raw[1][equals_pos + 2 :]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return (temp_c, temp_f)


@logger.catch
def scan_for_devices(directory):
    # Find all the devices that match the signature '28'
    temperature_devices = glob.glob(directory + "28*")
    # isolate the names of the individual devices
    device_list = []
    for device in temperature_devices:
        device_list.append(device)
    return device_list


@logger.catch
def read_temp(devices):
    """Poll each of the devices found and build a list of data."""
    measurements = []
    for i, device in enumerate(devices):
        # add the sub-directory name that holds the temperature data
        d = Path(device, "w1_slave")
        # open the file as readonly
        file_handle = open(d, "r")
        # gather the data
        lines = file_handle.readlines()
        file_handle.close()
        temps = calculate_temp(lines)
        # build the result output for this device
        celcius, farenheiht = temps
        out = {
            "TimeStamp": UTC_NOW_STRING(),
            "ID": f"ID# {Path(device).name}",
            "Celcius": f"{celcius:.2f}C",
            "Farenheiht": f"{farenheiht:.1f}F",
        }
        measurements.append(out)
    return (UTC_NOW_STRING(), measurements)


while True:
    devices = scan_for_devices(SPI_DEVICE_PATH)
    timestamp, device_data = read_temp(devices)
    print(timestamp)
    for device in device_data:
        print(device)
    write_csv(device_data, filename=timestamp, use_subs=True)
    time.sleep(6)
