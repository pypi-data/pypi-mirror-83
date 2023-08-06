"""
functions that clone project templates

author: murmuur
"""

import os
from shutil import copytree

def new_pyfile(destination, root_path):
    """
    Copies all files needed for a python project from template
    """
    template_path = root_path + '/templates/python'

    copytree(template_path, destination)
