#!/usr/bin/env python
# -*- coding: utf-8 -*-
# version 2.0
"""Standardize methods for file handling.
"""

from pathlib import Path
from loguru import logger

# set your reference point with the location of the python file you’re writing in
this_file = Path(__file__)

# Here are three ways to get the folder of the current python file
this_folder1 = Path(__file__, "..")
this_folder2 = Path(__file__) / ".."
this_folder3 = Path(__file__).parent

# This will fail becasue the variables are relative paths:
# assert this_folder1 == this_folder2 == this_folder3

# The resolve() method removes '..' segments, follows symlinks, and returns
# the absolute path to the item.
# this works:
# assert this_folder1.resolve() == this_folder2.resolve() == this_folder3.resolve()

# folder_where_python_was_run = Path.cwd()

# create a new folder:
# Path("/my/directory").mkdir(parents=True, exist_ok=True)

# project_root = Path(__file__).resolve().parents[1] # this is the folder 2 levels up from your running code.
# create a new PathObj:
# static_files = project_root / 'static' # if you like this sort of thing they overrode the divide operator.
# media_files = Path(project_root, 'media') # I prefer this method.

# how to define 2 sub-directories at once:
# compiled_js_folder = static_files.joinpath('dist', 'js') # this is robust across all OS.

# list(static_files.iterdir()) # returns a list of all items in directory.

# [x for x in static_files.iterdir if x.is_dir()] # list of only directories in a folder.

# [x for x in static_files.iterdir if x.is_file()] # same for files only.

# get a list of items matching a pattern:
# list(compiled_js_folder.glob('*.js')) # returns files ending with '.js'.

# search recursively down your folders path:
# sorted(project_root.rglob('*.js'))

# verify a path exists:
# Path('relative/path/to/nowhere').exists() # returns: False

# Example of directory deletion by pathlib
# pathobj = Path("demo/")
# pathobj.rmdir()

# Example of file deletion by pathlib
# pathobj = Path("demo/testfile.txt")
# pathobj.unlink()

""" access parts of a filename:
>>> Path('static/dist/js/app.min.js').name
'app.min.js'
>>> Path('static/dist/js/app.min.js').suffix
'.js'
>>> Path('static/dist/js/app.min.js').suffixes
'.min.js'
>>> Path('static/dist/js/app.min.js').stem
'app'
"""


@logger.catch
def clean_filename_str(fn):
    """Remove invalid characters from provided string."""
    # TODO replace invalid characters with underscores
    return "".join(i for i in fn if i not in "\/:*?<>|")


@logger.catch
def create_datebased_subdirectory_Structure(timestamp: str):
    """Takes a string (2020-10-05_020600UTC) representing a datetime 
    and attempts to create a directory structure 
    in the format ./YYYY/MM/DD/ and returns a Pathobj to the directory.
    """
    date, _time = timestamp.split('_') # split date from time
    yy, mm, dd = date.split('-')
    OP = f'{yy}/{mm}/{dd}/'
    return OP


@logger.catch
def check_and_validate(fname, direc, rename=True, use_subdirs=False):
    """Return a PathObj for this filename/directory.
    Fail if filename already exists in directory but optionally rename.
    """
    clean_fn = clean_filename_str(fname)
    direc.mkdir(parents=True, exist_ok=True)
    if use_subdirs:
        dest = create_datebased_subdirectory_Structure(clean_fn)
    else:
        dest = ""
    OUT_PATH = Path(direc, dest)
    OUT_PATH.mkdir(parents=True, exist_ok=True)
    i = 0
    while Path(OUT_PATH, clean_fn).exists():
        if rename:
            # TODO  strip old (#) from name and rename
            i += 1
            clean_fn = f"{clean_fn}({i})"
        else:
            raise FileExistsError
    return Path(OUT_PATH, clean_fn)


if __name__ == "__main__":
    from pathlib import Path
    this_file = Path(__file__)
    print(f'This file {this_file} has no current standalone function.')
