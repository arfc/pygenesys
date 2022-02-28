#! /usr/bin/env python

import numpy as np
import importlib
import inspect
import argparse
import os
import sys
import sqlite3

# custom imports
from pygenesys import model_info
from pygenesys.technology.technology import Technology
from pygenesys.commodity.commodity import *
from pygenesys.make_config import *


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


def collect_technologies(module_name):
    """
    Collects the technologies from the PyGenesys input file.

    Parameters
    ----------
    module_name : python module
        The PyGenesys input file once imported. Should be "infile."
    """
    technologies = []

    for member, attrib in inspect.getmembers(module_name):
        try:
            string_attr = str(attrib)
        except BaseException:
            string_attr = ''

        # if 'Technology' in string_attr:
        if isinstance(attrib, Technology):
            technologies.append(getattr(module_name, member))

    return technologies


def _collect_commodities(technology_list):
    """
    Collects the unique commodities from the PyGenesys input file.
    Each list of commodities (demand, resource, emission) should be
    a unique set. Numpy.unique cannot compare objects, so an empty
    dictionary is initialized and populated with Commodity names
    for keys and Commodity objects for values. Therefore only unique
    commodities will be returned.

    NOTE: This function fails to collect all commodities. Commodities must
    be explicitly listed in the input file for now!


    This function should be extended to account for cases where
    the input and output commodities are lists (i.e. when there's
    a ``techinputsplit``).
    """

    demand = {}
    resource = {}
    emission_dict = {}

    for tech in technology_list:
        for region in tech.regions:
            print(f'REGION: {region}')
            input_comm = tech.input_comm[region]
            output_comm = tech.output_comm[region]

            print(f'Commodity types for {tech.tech_name}')
            print(f"{type(input_comm)}")
            print(f"{type(output_comm)}")
            # check the input commodity type
            if isinstance(input_comm, Commodity):
                # resource
                if input_comm.comm_name not in resource:
                    resource[input_comm.comm_name] = input_comm
                    continue
                else:
                    continue
            elif isinstance(input_comm, list):
                for comm in input_comm:
                    if (isinstance(comm, Commodity)) and \
                       (comm.comm_name not in resource):
                        resource[comm.comm_name] = comm
                    else:
                        continue
            else:
                print(f'Input commodity for {tech.tech_name} in {region} '
                      'is not a resource. Check input file.')

            if isinstance(output_comm, DemandCommodity):
                # demand
                demand[output_comm.comm_name] = output_comm
            elif isinstance(output_comm, Commodity):
                # resource
                if output_comm.comm_name not in resource:
                    resource[output_comm.comm_name] = output_comm
                    continue
                else:
                    continue

            elif isinstance(output_comm, EmissionsCommodity):
                # emission
                print(f"Warning: Output commodity of {tech.tech_name}"
                      f"is an Emission Commodity. Check input file.")
                continue
            try:
                emissions = tech.emissions[region]
                print(f"{type(emissions)}")

                # loop through emissions commodities
                for emis in list(emissions.keys()):
                    if (isinstance(emis, EmissionsCommodity)) and \
                       (emis.comm_name not in emission_dict):
                        emission_dict[emis.comm_name] = emis
                    else:
                        continue
            except BaseException:
                pass

    resources = list(resource.values())
    demands = list(demand.values())
    emissions_list = list(emission_dict.values())

    if len(demands) == 0:
        print('Warning: Input file has no technologies that satisfy demands.')
        print('No demands written to database. Consider adding a transmission'
              'technology.')

    return resources, demands, emissions_list


def main():

    # Read commandline arguments
    parser = argparse.ArgumentParser(description='PyGenesys Parameters')
    parser.add_argument('--infile', help='the name of the input file')
    args = parser.parse_args()
    print(f"Reading input from {args.infile} \n")

    infile = load_infile(args.infile)
    out_db = infile.database_filename
    try:
        out_path = infile.curr_dir + "/" + out_db
    except BaseException:
        out_path = "./" + out_db

    # get infile technologies
    technology_list = collect_technologies(infile)



    # create the model object
    model = model_info.ModelInfo(output_db=out_path,
                                 scenario_name=infile.scenario_name,
                                 start_year=infile.start_year,
                                 end_year=infile.end_year,
                                 N_years=infile.N_years,
                                 N_seasons=infile.N_seasons,
                                 N_hours=infile.N_hours,
                                 demands=infile.demands_list,
                                 resources=infile.resources_list,
                                 emissions=infile.emissions_list,
                                 technologies=technology_list,
                                 reserve_margin=infile.reserve_margin,
                                 global_discount=infile.discount_rate
                                 )
    print(f"Database will be exported to {model.output_db} \n")


    model._write_sqlite_database()

    print("Input file written successfully.\n")

    # create the config file
    print("Writing Temoa config file.\n")

    config_template = 'config_template.txt'
    fname = name_from_path(out_db)
    print(f'File name: {fname}\n')
    conf_name = f'run_{fname}.txt'
    vars = {'target_dir':infile.folder,
            'file_name':fname+'.sqlite',
            'scenario':infile.scenario_name}

    # outpath should be one folder up.
    path = infile.curr_dir
    print(f'{infile.curr_dir}\n')
    print(f'{path}\n')
    rendered = render_input(input_path='default',
                            input_fname='default',
                            variable_dict=vars,
                            output_path=path,
                            output_fname=conf_name)

    return
