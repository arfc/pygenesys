import pandas as pd
import numpy as np
import os
from datetime import date

months = ['january',
          'february',
          'march',
          'april',
          'may',
          'june',
          'july',
          'august',
          'september',
          'october',
          'november',
          'december']

eia_techs = ['Petroleum Liquids', 'Onshore Wind Turbine',
            'Conventional Hydroelectric', 'Natural Gas Steam Turbine',
            'Conventional Steam Coal', 'Natural Gas Fired Combined Cycle',
            'Natural Gas Fired Combustion Turbine', 'Nuclear',
            'Hydroelectric Pumped Storage',
            'Natural Gas Internal Combustion Engine', 'Batteries',
            'Solar Photovoltaic', 'Geothermal', 'Wood/Wood Waste Biomass',
            'Coal Integrated Gasification Combined Cycle', 'Other Gases',
            'Petroleum Coke', 'Municipal Solid Waste', 'Landfill Gas',
            'Natural Gas with Compressed Air Storage', 'All Other',
            'Other Waste Biomass', 'Solar Thermal without Energy Storage',
            'Other Natural Gas', 'Solar Thermal with Energy Storage',
            'Flywheels', 'Offshore Wind Turbine']


def get_date():
    """
    Returns the current day, month, and year.
    """
    today = date.today().strftime("%B %d, %Y")

    today = today.split(' ')

    month = today[0]
    day = today[1]
    year = today[2]

    return month, day, int(year)


def capitalize_string(name_string):
    """
    This function capitalizes each word in a string of multiple
    words, representing the name of a place or technology.

    Example:
    >>> my_string = "lake county"
    >>> cap_string = capitalize_string(my_string)
    'Lake County'
    
    Parameters
    ----------
    name_string : string
        String to be capitalized.

    Returns
    -------
    cap_string : string
        Capitalized string.
    """
    cap_string = name_string
    cap_string = cap_string.split(' ')
    cap_string = [i.capitalize() for i in cap_string]
    cap_string = ' '.join(cap_string)

    return cap_string


def get_eia_generators(month=None, year=None):
    """
    This function returns a pandas dataframe containing information on
    all electric generators in the United States from a recent EIA form
    860M. Note: EIA forms are often delayed therefore this function
    subtracts four months from the current month to guarantee the file
    exists to be downloaded.

    Parameters
    ----------
    month : string
        The month of interest
    year : string
        The year of interest

    Returns
    -------
    df : pandas dataframe
        Holds the data from EIA form 860M
    """
    columns = [
        'Entity ID',
        'Entity Name',
        'Plant Name',
        'Sector',
        'Plant State',
        'Nameplate Capacity (MW)',
        'Technology',
        'Operating Year',
        'Status',
        'Balancing Authority Code',
        'County'
    ]

    # initialize with invalid options
    m = 'thermidor'
    y = 2

    if (month is None) and (year is None):
        m, d, y = get_date()
        month_idx = months.index(m.lower())
        month_idx -= 4
        if month_idx < 0:
            y -= 1
        m = months[month_idx]

    elif (month is not None) and (year is not None):
        print(f"Retrieving EIA Form 860m for {month.capitalize()} {year}")
        m = month
        y = year

    elif ((month is None) or (year is None)):

        print(f"Month {month} / Year {year}")
        raise ValueError(("Please specify a month and a year."))

    url = (f"https://www.eia.gov/electricity/data/eia860m/archive/xls/" +
           f"{m}_generator{y}.xlsx")

    try:
        print(f'Downloading from {url}\n')
        df = pd.read_excel(url,
                           sheet_name='Operating',
                           skipfooter=2,
                           skiprows=2,
                           usecols=columns,
                           index_col='Entity ID')
        print('Download successful.')
    except BaseException:
        print('Download failed. Trying different sheet format.')
        try:
            df = pd.read_excel(url,
                               sheet_name='Operating',
                               skipfooter=2,
                               skiprows=1,
                               usecols=columns,
                               index_col='Entity ID')
            print('Download successful.')
        except ValueError:
            fail_str = (f'Download failed. File not found' +
                        f' for Month: {month} and Year: {year}')
            raise ValueError(fail_str)

    return df


def get_region_techs(df, region):
    """
    Gets the existing capacity for a particular technology and region.
    Currently, only electric capacity is considered.

    Parameters
    ----------
    df : pandas dataframe
        The dataframe for EIA form 860M
    region : string
        The region of interest. Region may be state or county. The state must
        be given as a two letter abbreviation and a county must be provided as
        a full name.
    """

    if len(region) == 2:
        valid_state = (region.upper() in df['Plant State'].values)
        if valid_state:
            region_mask = df['Plant State'] == region.upper()
        else:
            raise ValueError(
                f'Detected state abbreviation.' +
                f' Abbreviation {region} not found.')
    else:
        valid_county = (capitalize_string(region) in df['County'].values)
        if valid_county:
            region_mask = df['County'] == capitalize_string(region)
        else:
            raise ValueError(
                f'Detected county name. County name {region} not found.')

    region_df = df[region_mask]

    return region_df


def get_tech(df, technology):
    """
    Gets the existing capacity for a particular technology for all regions.
    Currently, only electric capacity is considered.

    Parameters
    ----------
    df : pandas dataframe
        The dataframe for EIA form 860M
    technology : string
        The technology of interest. Accepts:
        ['Petroleum Liquids', 'Onshore Wind Turbine',
       'Conventional Hydroelectric', 'Natural Gas Steam Turbine',
       'Conventional Steam Coal', 'Natural Gas Fired Combined Cycle',
       'Natural Gas Fired Combustion Turbine', 'Nuclear',
       'Hydroelectric Pumped Storage',
       'Natural Gas Internal Combustion Engine', 'Batteries',
       'Solar Photovoltaic', 'Geothermal', 'Wood/Wood Waste Biomass',
       'Coal Integrated Gasification Combined Cycle', 'Other Gases',
       'Petroleum Coke', 'Municipal Solid Waste', 'Landfill Gas',
       'Natural Gas with Compressed Air Storage', 'All Other',
       'Other Waste Biomass', 'Solar Thermal without Energy Storage',
       'Other Natural Gas', 'Solar Thermal with Energy Storage',
       'Flywheels', 'Offshore Wind Turbine']
    """

    technology = capitalize_string(technology)

    valid_technology = (technology in df['Technology'].values)
    if valid_technology:
        tech_mask = df['Technology'] == technology
        tech_df = df[tech_mask]
    else:
        raise ValueError(f"Technology {technology} does not exist within specified region.\n"+
                         f"The following technologies are accepted:\n"+
                         f"{eia_techs}")

    return tech_df


def get_existing_capacity(df, region, technology):
    """
    Gets the existing capacity for a particular technology and region.
    Currently, only electric capacity is considered.
    If the user has an internet connection, PyGenesys will attempt to collect
    the most up-to-date electric generator data. Otherwise, PyGenesys will
    default to the data stored in ``pygenesys.data.library``.
    Users can also specify a month and year to obtain a specific historical
    dataset from EIA.
    Parameters
    ----------
    df : pandas dataframe
        The dataframe for EIA form 860M
    region : string
        The region of interest. Region may be state or county. The state must
        be given as an abbreviation a county must be provided as a full name.
    technology : string
        The electric generating technology of interest. E.g. "Nuclear"
    Returns
    -------
    existing_capacity : dictionary
        A dictionary containing existing capacity with years
        as keys and capacity, in MW, as values.
    """
    # filter by region
    df = get_region_techs(df, region=region)

    # filter by technology
    tech_df = get_tech(df, technology)

    sorted_tech_df = tech_df.sort_values(by=['Operating Year'])
    sorted_tech_df.set_index('Operating Year', inplace=True)
    sorted_tech_df.index = pd.to_datetime(sorted_tech_df.index, format='%Y')
    sorted_tech_df = sorted_tech_df.resample('Y').sum()

    year_filter_df = sorted_tech_df[sorted_tech_df['Nameplate Capacity (MW)'] > 0.0]

    existing_capacity = dict(zip(year_filter_df.index.year.values,
                                year_filter_df['Nameplate Capacity (MW)'].values))

    return existing_capacity
