#!/usr/bin/env python
# -*- coding: utf-8 -*-
# version 2.0
"""Create a file and populate with items from a data structure.
"""

import csv
from pathlib import Path
from filehandling import clean_filename_str
from loguru import logger
from time_strings import UTC_NOW_STRING

"""'data' is expected to be a list of dicts 
# TODO expand functionality to work with pandas dataframes.
Process: file exist? headers match? append data.
file exist? headers mis-match. raise exception
no file? create file and save data.
"""


@logger.catch
def write_csv(data, directory="CSV_DATA", ts=None, use_cwd=True):
    """Accepts a list of dicts and writes data as CSV in location specified.
    # TODO add ability to process pandas_dataframes as well as lists of dicts.
    This list can contain multiple readings of one device or multiple devices.
    Each device will be written to a different CSV file and will be appended to any existing file.
    # TODO add timestamp parameter to use as directory structure hint.
    #   if timestamp leads to an existing file location then append data to existng file.
    Args:
        data (a list of dicts): This list should contain readings of one device or multiple devices.
            dicts contain all relative device data
        directory (str, optional): Sub-directory off of current working directory. Defaults to "CSV_DATA".
    """
    if ts == None: 
        ts = UTC_NOW_STRING 
    # create csv file path
    # TODO use root directory if use_cwd is False
    dirobj = Path(Path.cwd(), directory)
    dirobj.mkdir(parents=True, exist_ok=True)

    # examine data for each unique entry and place into a dictionary as a list of lists
    readings_dict = {}
    for item in data:
        if type(item) != dict:
            raise ValueError(f"Expected dict got {type(item)}")
        device, temp, timestmp, raw, name, = "", "", "", "", ""
        for key, val in item.items():
            if key == "ID":
                device = str(val)
            if key == "Celcius":
                temp = str(val)
            if key == "TimeStamp":
                timestmp = str(val)
            if key == "RAW DATA":
                raw = str(val)
            if key == "Location":
                name = str(val)                
        if device not in readings_dict.keys():
            readings_dict[device] = []
        readings_dict[device].append([timestmp, temp, name, raw])

    if len(readings_dict) < 1:
        raise Exception(f"No temperature readings found in supplied data.")
    print(f'Readings Dict: {readings_dict}')
    for key, val in readings_dict.items():
        print(f'key: {key} value: {val}')
        fname = f"{clean_filename_str(str(key))}_{val[0][2]}.CSV"
        pathobj = Path(dirobj, fname)
        if not pathobj.exists():
            with open(pathobj, "w", newline="") as csvfile:
                csv_obj = csv.writer(csvfile, delimiter=",")
                csv_obj.writerow(["Timestamp", "Reading", "Location", "RAW DATA"])
        with open(pathobj, "a+", newline="") as csvfile:
            csv_obj = csv.writer(csvfile, delimiter=",")
            for item in val:  # val should be the list of lists contaning time and temp.
                csv_obj.writerow(item)
    return True


if __name__ == "__main__":
    this_file = Path(__file__)
    print(f"This file {this_file} has no current standalone function.")
