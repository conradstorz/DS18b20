#!/usr/bin/env python
# -*- coding: utf-8 -*-
# version 2.0
"""Create a file and populate with items from a data structure.
"""

import csv
from pathlib import Path
from filehandling import clean_filename_str
from loguru import logger

"""'data' is expected to be a list of dicts 

Process: file exist? headers match? append data.
file exist? headers mis-match. raise exception
no file? create file and save data.
"""


@logger.catch
def write_csv(data, device_names, directory="CSV_DATA"):
    """Accepts a list of dicts and writes data as CSV in location specified.
    This list can contain multiple readings of one device or multiple devices.
    Each device will be written to a different CSV file and will be appended to any existing file.

    Args:
        data (a list of dicts): This list can contain multiple readings of one device or multiple devices.
        device_names (dict): Known devices names in 'ID:Name' format
        directory (str, optional): Sub-directory off of current working directory. Defaults to "CSV_DATA".
    """
    # create csv file path
    dirobj = Path(Path.cwd(), directory)
    dirobj.mkdir(parents=True, exist_ok=True)

    # examine data for each unique entry and place into a dictionary as a list of lists
    readings_dict = {}
    for item in data:
        if type(item) != dict:
            raise ValueError(f"Expected dict got {type(item)}")
        device, temp, timestmp, raw = "", "", "", ""
        for key, val in item.items():
            if key == "ID":
                device = str(val)
            if key == "Celcius":
                temp = str(val)
            if key == "TimeStamp":
                timestmp = str(val)
            if key == "RAW DATA":
                raw = str(val)
        if device not in readings_dict.keys():
            readings_dict[device] = []
        readings_dict[device].append([timestmp, temp, raw])

    if len(readings_dict) < 1:
        raise Exception(f"No temperature readings found in supplied data.")
    for key, val in readings_dict.items():
        if key in device_names.keys():
            fname = f"{clean_filename_str(str(key))}_{device_names[key]}.CSV"
        else:
            fname = f"{clean_filename_str(str(key))}_UNIDENTIFIED.CSV"
        pathobj = Path(dirobj, fname)
        if not pathobj.exists():
            with open(pathobj, "w", newline="") as csvfile:
                csv_obj = csv.writer(csvfile, delimiter=",")
                csv_obj.writerow(["Timestamp", "Reading", "RAW DATA"])
        with open(pathobj, "a+", newline="") as csvfile:
            csv_obj = csv.writer(csvfile, delimiter=",")
            for item in val:  # val should be the list of lists contaning time and temp.
                csv_obj.writerow(item)
    return True


if __name__ == "__main__":
    this_file = Path(__file__)
    print(f"This file {this_file} has no current standalone function.")
