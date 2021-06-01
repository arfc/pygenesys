#! /usr/bin/env python

import numpy as np
import importlib
import argparse
import os, sys
import sqlite3

def name_from_path(infile_path):
    """
    Returns just the base of the filename from the path.

    Parameters
    ----------
    infile_path : string
        The path to PyGenesys input file
        (absolute, relative, or missing extensions are okay)

    Returns
    -------
    file_name_base : string
        The base name without the extension or path
    """
    file_dir = os.path.dirname(infile_path)
    sys.path.append(file_dir)
    file_name = os.path.basename(infile_path)
    file_name_base = os.path.splitext(file_name)[0]
    return file_name_base


def load_infile(infile_path):
    """
    Loads the input file as a python package import based on the path.

    Parameters
    ----------
    infile_path : string
        The path to the PyGenesys input file.

    Returns
    -------
    infile : Python module
        The PyGenesys input file imported as a python
        module.
    """
    file_name = name_from_path(infile_path)
    infile = importlib.import_module(file_name)
    return infile


def main():

    # Read commandline arguments
    ap = argparse.ArgumentParser(description='PyGenesys Parameters')
    ap.add_argument('--infile', help='the name of the input file')
    args = ap.parse_args()
    print(f"Reading input from {args.infile} \n")

    infile = load_infile(args.infile)
    out_db = infile.database_filename
    out_path = infile.curr_dir + "/" + out_db

    print(f"Database will be exported to {out_path} \n")

    print("The main function")

    return
