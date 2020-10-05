#!/usr/bin/env python
# -*- coding: utf-8 -*-
# version 2.0
"""Create a file and populate with items from a data structure.
"""

import csv
from pathlib import Path
from filehandling import check_and_validate
from loguru import logger


@logger.catch
def write_csv(data, filename="temp.csv", directory="CSV_DATA", use_subs=False):
    """'data' is expected to be a list of dicts 
    Take data and write all fields to storage as csv with headers from keys.
    """
    # create csv file path
    dirobj = Path(Path.cwd(), directory)
    dirobj.mkdir(parents=True, exist_ok=True)    
    pathobj = check_and_validate(filename, dirobj, use_subdirs=use_subs)

    with open(pathobj, "w", newline="") as csvfile:
        if type(data) == list and type(data[0]) == dict:
            headers = data[0].keys()
        else:
            headers = ["No DATA found."]
        # creating a csv dict writer object
        writer = csv.DictWriter(csvfile, fieldnames=headers)            
        # writing headers (field names)
        writer.writeheader()
        # writing data rows
        writer.writerows(data)

    return



if __name__ == "__main__":
    from pathlib import Path
    this_file = Path(__file__)
    print(f'This file {this_file} has no current standalone function.')
