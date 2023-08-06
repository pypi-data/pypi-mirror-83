"""
Global functions for package

author: murmuur
"""

import os, configparser

def is_valid_path(file_path):
    """
    Gets contents in file given a relative path to where command was run

    Note: confidently works on macos file system, others unknown
    """
    if os.path.exists(file_path):
        raise FileExistsError("File already exists at location ... " + file_path)
    if os.path.isfile(file_path):
        raise NotADirectoryError("Not a directory at location ... " + file_path)
