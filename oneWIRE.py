#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This is version 2 of the 1wire(spi) program.
This version introduces expanded ThingSpeak functionality. Specifically ThingSpeak only allows a max of 8 datapoints.
When more than 8 data monitoring points exist, this program will have the ability to send individual points to
specified ThingSpeak Channels.
# TODO permit a reading be sent to multiple channels.
"""
DEBUG = True

from pathlib import Path
import glob
import time
import json
from time_strings import UTC_NOW_STRING
from oneWIRE_dict2csv import write_csv
from loguru import logger
import urllib.request
import collections
import random
from tqdm import tqdm
import cfsiv_utils.filehandling as fh

oneWIRE_DEVICE_PATH = "/sys/bus/w1/devices/"
oneWIRE_DEVICE_NAMES_FILE = "oneWIRE_devices.json"
OUTPUT_ROOT = 'CSV_DATA/'
DEBUG_MOCK_DEVICES = ['device/28egcwharxan', 'device/28iyrsngfmrahuh']

THINGSPEAK_WRITEKEY = '3Z8YHDG350XFO9I4'
THINGSPEAK_WRITE_URL = f'https://api.thingspeak.com/update?api_key=' # requires a writekey and field values appended here

DEVICE_DESCRIPTIONS = {}
DESCRIPTIONS_MODIFIED = None


@logger.catch()
def Configure_logging():
    # Logging Setup
    logger.remove()  # removes the default console logger provided by Loguru.
    # I find it to be too noisy with details more appropriate for file logging.
    # INFO and messages of higher shown on the console.
    logger.add(lambda msg: tqdm.write(msg, end=""), format="{message}", level="INFO")
    # This creates a logging sink and handler that puts all messages at or above the TRACE level 
    # into a logfile for each run.
    logger.add(
        "./LOGS/file_{time}.log", level="TRACE", encoding="utf8"
    )  # Unicode instructions needed to avoid file write errors.
    return None



@logger.catch
def retreive_device_names():
    """Updates GLOBAL data describing device names.

    Returns:
        nothing: effect is GLOBAL
    """
    global DEVICE_DESCRIPTIONS, DESCRIPTIONS_MODIFIED
    global_device_names_file = Path(oneWIRE_DEVICE_NAMES_FILE)
    # check to see if descriptions have changed and re-load
    modified = (global_device_names_file.stat().st_atime)  
    # atime, mtime, ctime don't seem to mean what I think. (Windows idicy)
    if DESCRIPTIONS_MODIFIED != modified:
        DESCRIPTIONS_MODIFIED = modified
        logger.info("Device names have been updated. Re-loading...")
        try:
            with open(global_device_names_file) as json_data:
                DEVICE_DESCRIPTIONS = json.load(json_data)
                # this dictionary will contain information about individual known devices                
        except json.decoder.JSONDecodeError as e:
            logger.info(f'Error reading JSON file: {e}')

    return None


@logger.catch
def calculate_temp(raw, min=-29, max=260):
    """Accepts raw output of DS18b20 sensor.
    Minimum and Maximum values can be specified to filter out noisy bad results.
    Returns a tuple of temp in C and F. 
    Output truncated at 2 decimals precision.
    """
    # TODO sanitize and validate min/max variables against bad user input.
    equals_pos = -1
    if len(raw) >= 2:
        equals_pos = raw[1].find("t=")
        # logger.info(f'Equals position: {equals_pos}')
    if equals_pos != -1:
        temp_string = raw[1][equals_pos + 2 :]
        temp_c = round(float(temp_string) / 1000.0, 2)        
        if temp_c < float(min): temp_c = float(min)
        if temp_c > float(max): temp_c = float(max)
        logger.info(f'Temperature string: {temp_string}')
        temp_f = round(temp_c * 9.0 / 5.0 + 32.0, 2)
        return (temp_c, temp_f)
    return (0,0)


@logger.catch
def Detect_Devices(directory=oneWIRE_DEVICE_PATH):
    """Searches default debian-linux psuedo-directory where oneWIRE Interface devices are described.

    Args:
        directory (str, optional): [description]. Defaults to oneWIRE_DEVICE_PATH.

    Returns:
        list: a list of the device names found
    """
    # Find all the devices that match the signature '28'
    if DEBUG:
        temperature_devices = DEBUG_MOCK_DEVICES
    else:
        temperature_devices = glob.glob(directory + "28*")
    # logger.info(f'Devices: {temperature_devices}')

    # isolate the names of the individual devices
    device_list = []
    for device in temperature_devices:
        parts = device.split("/")
        # logger.info(f'Parts: {parts}')
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
    # TODO Add sanity checks to temperature data
    global DEVICE_DESCRIPTIONS
    measurements = []
    if len(devices) > 0:
        for _idx, device in enumerate(devices): # ignore the index value
            # add the sub-directory name that holds the temperature data
            dev_path = Path(oneWIRE_DEVICE_PATH, device, "w1_slave")
            try:
                with open(dev_path, "r") as dev_data:
                    lines = dev_data.readlines()
            except FileNotFoundError as e:
                logger.info(f'Device file not found: {e}')
                lines = ['garbage', f'dummy t={random.random()*100000}']
            Celsius, farenheiht = calculate_temp(lines)
            try:
                dev = DEVICE_DESCRIPTIONS[device]
                location_name = f"{dev['Name']}"
                channel = f"{dev['THINGSPEAK_Channel']}"
                field = f"{dev['THINGSPEAK_Field']}"
            except KeyError as e:
                logger.info(f'KeyError reading devices: {e}')
                location_name = "UNKNOWN"
                channel = "UNSPECIFIED"
                field = 0
            out = {
                "TimeStamp": UTC_NOW_STRING(),
                "ID": f"{Path(device).name}",
                "Location": location_name,
                "Celsius": f"{Celsius:.2f}",
                "Farenheiht": f"{farenheiht:.1f}",
                "THINGSPEAK_Field": field,
                "THINGSPEAK_Channel": channel,
                "RAW DATA": lines,
            }
            if Celsius == farenheiht:
                # Only -40 would be an exact match and this program ignores temps that low.
                # If they are equal it is because they both are Zero which is impossible.
                logger.info('Error obtaining temperature readings.')
            else:
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
            channel = ""
            # channel = str(input(f'Would you like to enter a channel for device {device}?'))
            if len(channel) <= 0:
                channel = "UNSPECIFIED"
            field = ""
            # field = str(input(f'Would you like to enter a field for device {device}?'))
            if len(field) <= 0:
                field = "0"
            DEVICE_DESCRIPTIONS[device] = {'Name': name, 'THINGSPEAK_Channel': channel, 'THINGSPEAK_Field': field}
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
def send_to_thingspeak(data):
    """Send readings to ThingSpeak server.

    Args:
        data (list): A list of dicts of device polling results.
       
    Returns:
        Nothing
    """
    sorted_dev_data = sorted(data, key=lambda k: k['THINGSPEAK_Channel'])
    split_by_channel = collections.defaultdict(list)
    for d in sorted_dev_data:
        split_by_channel[d['THINGSPEAK_Channel']].append(d)
    channel_list = list(split_by_channel.values())
    if len(channel_list) <= 0: # we have not found channel data
        raise IOError('No data channels found.')
    for channel in channel_list:
        fields = ''
        TS_Channel = ''
        for _idx, device_dict in enumerate(channel):
            field_tag = f'&field{device_dict["THINGSPEAK_Field"]}={device_dict["Farenheiht"]}'
            fields = f'{fields}{field_tag}'
            TS_Channel = device_dict["THINGSPEAK_Channel"]
        if TS_Channel == 'DUMMY':
            url = 'Dont_send_anything.com'
        else:
            url = f'{THINGSPEAK_WRITE_URL}{TS_Channel}{fields}'
        logger.info(url)
        if DEBUG:
            logger.info(f'URL={url} [not sent].')
        else:
            try:
                with urllib.request.urlopen(url) as response:
                    html = response.read()
            except (urllib.error.HTTPError, ValueError) as e:
                logger.info(f'Bad URL: {e}')
    return None


@logger.catch
def main_data_gathering_loop():
    while True:
        retreive_device_names()
        devices = check_devices_have_names()
        if len(devices) > 0:
            try:
                timestamp, device_data = Read_Device(devices)
            except IOError as e:
                logger.info(f'Devices not responding: {e}')
            else:
                output_directory = create_timestamp_subdirectory_Structure(timestamp)
                OD = f"{OUTPUT_ROOT}{output_directory}"
                for device in device_data:
                    logger.info(device)
                write_csv(device_data, directory=OD)
                send_to_thingspeak(device_data)
        else:
            logger.info("No devices found.")
        logger.info("Sleeping 10 seconds...")
        time.sleep(10)


@logger.catch
def check_devices_have_names():
    global DEVICE_DESCRIPTIONS
    devices = check_names_of_devices()
    with open(oneWIRE_DEVICE_NAMES_FILE, "w") as json_outfile:
        json.dump(DEVICE_DESCRIPTIONS, json_outfile, indent=4)
    return devices


if __name__ == "__main__":
    Configure_logging()
    main_data_gathering_loop()
