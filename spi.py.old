#!/usr/bin/env python
# -*- coding: utf-8 -*-

SPI_DEVICE_PATH = "/sys/bus/w1/devices/"
SPI_DEVICE_NAMES_FILE = "SPI_devices.json"
OUTPUT_ROOT = 'CSV_DATA/'

THINGSPEAK_WRITEKEY = '3Z8YHDG350XFO9I4'
THINGSPEAK_FIELD1 = 'field1'
THINGSPEAK_FIELD2 = 'field2'
THINGSPEAK_FIELD3 = 'field3'
THINGSPEAK_FIELD4 = 'field4'
THINGSPEAK_WRITE_URL = f'https://api.thingspeak.com/update?api_key={THINGSPEAK_WRITEKEY}'

from pathlib import Path
import glob
import time
import json
from time_strings import UTC_NOW_STRING
from dev_dict2csv import write_csv
from loguru import logger
import urllib.request

DEVICE_DESCRIPTIONS = None
DESCRIPTIONS_MODIFIED = None


@logger.catch
def retreive_device_names():
    """Updates GLOBAL data describing device names.

    Returns:
        nothing: effect is GLOBAL
    """
    global DEVICE_DESCRIPTIONS, DESCRIPTIONS_MODIFIED
    fn = Path(SPI_DEVICE_NAMES_FILE)
    # check to see if descriptions have changed and re-load
    modified = (
        fn.stat().st_atime
    )  # atime, mtime, ctime don't seem to mean what I think. (Pathlib error?)
    if DESCRIPTIONS_MODIFIED != modified:
        DESCRIPTIONS_MODIFIED = modified
        print("Device names have been updated. Re-loading...")
        with open(fn) as json_data:
            DEVICE_DESCRIPTIONS = json.load(json_data)
            # this dictionary will contain information about individual known devices
    return None


@logger.catch
def calculate_temp(raw):
    """Accepts raw output of DS18b20 sensor and returns a tuple of temp in C and F."""
    equals_pos = -1
    if len(raw) >= 2:
        equals_pos = raw[1].find("t=")
    if equals_pos != -1:
        temp_string = raw[1][equals_pos + 2 :]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return (temp_c, temp_f)
    else:
        return (0,0)


@logger.catch
def Detect_Devices(directory=SPI_DEVICE_PATH):
    """Searches default debian-linux psuedo-directory where Single Pin Interface (SPI) are described.

    Args:
        directory (str, optional): [description]. Defaults to SPI_DEVICE_PATH.

    Returns:
        list: a list of the device names found
    """
    # Find all the devices that match the signature '28'
    temperature_devices = glob.glob(directory + "28*")
    # isolate the names of the individual devices
    device_list = []
    for device in temperature_devices:
        parts = device.split("/")
        d = parts[-1:]
        # d is a list with only one string inside
        device_list.append(d[0])
    return device_list


@logger.catch
def Read_Device(devices: list):
    """Poll one or more devices provided and return status including environment reading.

    Args:
        devices (list): A list of device identifiers (system names) to poll.

    Returns:
        tuple: (UTC time as string, a list of dicts contaning device status)
    """
    measurements = []
    if len(devices) > 0:
        for i, device in enumerate(devices):
            # add the sub-directory name that holds the temperature data
            dev_path = Path(SPI_DEVICE_PATH, device, "w1_slave")
            with open(dev_path, "r") as dev_data:
                lines = dev_data.readlines()
            celcius, farenheiht = calculate_temp(lines)
            try:
                location_name = f"{DEVICE_DESCRIPTIONS[device]}"
            except KeyError:
                location_name = "UNKNOWN"
            out = {
                "TimeStamp": UTC_NOW_STRING(),
                "ID": f"{Path(device).name}",
                "Location": location_name,
                "Celcius": f"{celcius:.2f}",
                "Farenheiht": f"{farenheiht:.1f}",
                "RAW DATA": lines,
            }
            measurements.append(out)
        if len(measurements) <= 0:
            raise IOError('No measurements found.')
    else:
        raise IOError('No Devices declared.')

    return (UTC_NOW_STRING(), measurements)


@logger.catch
def check_names_of_devices():
    """Take the list of device identifiers and compare to the file of known devices.
    For items not found to have been previously named, allow interactive naming by operator.
    """
    global DEVICE_DESCRIPTIONS
    devices = Detect_Devices()
    for device in devices:
        if device not in DEVICE_DESCRIPTIONS.keys():
            name = ""
            # name = str(input(f'Would you like to enter a name for device {device}?'))
            if len(name) <= 0:
                name = "UNDEFINED"
            DEVICE_DESCRIPTIONS[device] = name
    return devices


@logger.catch
def create_timestamp_subdirectory_Structure(timestamp: str):
    """Takes a string (2020-10-05_020600UTC) representing a datetime
    and attempts to create a directory structure
    in the format ./YYYY/MM/DD/ and returns a Pathobj to the directory.
    """
    date, time = timestamp.split("_")  # split date from time
    yy, mm, dd = date.split("-")
    _hh = time[:2]
    OP = f"{yy}/{mm}/{dd}/"
    return OP


@logger.catch
def send_to_thingspeak(data, names):
    """Send readings to ThingSpeak server.

    Returns:
        Nothing
    """
    fields = ''
    for idx, device in enumerate(data):
        fields = f'{fields}&field{idx+1}={device["Farenheiht"]}'
    url = f'{THINGSPEAK_WRITE_URL}{fields}'
    print(url)
    with urllib.request.urlopen(url) as response:
        html = response.read()


@logger.catch
def main_data_gathering_loop():
    while True:
        retreive_device_names()
        devices = check_devices_have_names()
        if len(devices) > 0:
            try:
                timestamp, device_data = Read_Device(devices)
            except IOError as e:
                print('Devices not responding.')
            output_directory = create_timestamp_subdirectory_Structure(timestamp)
            OD = f"{OUTPUT_ROOT}{output_directory}"
            for device in device_data:
                print(device)
            write_csv(device_data, DEVICE_DESCRIPTIONS, directory=OD)
            send_to_thingspeak(device_data, DEVICE_DESCRIPTIONS)
        else:
            print("No devices found.")
        print("Sleeping 6 seconds...")
        time.sleep(6)


@logger.catch
def check_devices_have_names():
    devices = check_names_of_devices()
    with open(SPI_DEVICE_NAMES_FILE, "w") as json_outfile:
        json.dump(DEVICE_DESCRIPTIONS, json_outfile)
    return devices


@logger.catch
def report_history(start, end):
    """Returns data for readings recorded between start and end.

    Args:
        start (Timestamp): beginning of period of interest
        end (Timestamp): end of period of interest
    """
    # read files covering time period
    start_dir = create_timestamp_subdirectory_Structure(start)
    end_dir = create_timestamp_subdirectory_Structure(end)
    parts_start = start_dir.split('/')
    parts_end = end_dir.split('/')
    # TODO improve locating of files that match the given timeframe
    # This search routine is not accurate enough
    if parts_start[0] == parts_end[0]: # years match
        if parts_start[1] == parts_end[1]: # months and year match
            if parts_start[2] == parts_end[2]: # day of month and year match
                pass
                # pandas load files from single day directory
            else:
                pass
                # pandas load files from all days of month
        else:
            pass
            # pandas load files from all months of year 
    else:
        pass
        # pandas load files from all sub-diectories of OUTPUT_ROOT

    # process data

    # return data in pandas dataframe
    return


if __name__ == "__main__":
    main_data_gathering_loop()
