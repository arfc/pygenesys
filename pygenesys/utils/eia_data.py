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



def get_date():
    """
    Returns the current day, month, and year.
    """
    today = date.today().strftime("%B %d, %Y")

    today = today.split(' ')

    month = today[0]
    day = today[1]
    year = today[2]

    return month, day, year

def get_eia_generators(month=None, year=None):
    """
    This function returns a pandas dataframe containing information on
    all electric generators in the United States. EIA form 860m

    Parameters
    ----------
    month : string
        The month of interest
    year : string
        The year of interest

    Returns
    -------
    df : pandas dataframe
        Holds the data from EIA form 860m
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

    if (month == None) and (year == None):
        m, d, y = get_date()
        month_idx = months.index(m.lower())
        month_idx -= 4
        if month_idx < 0:
            y -= 1
        m = months[month_idx]


    elif (month == None) and (year != None):
        print("no month given, year given")
        pass

    elif (month != None) and (year != None):
        print("date given")
        m = month
        y = year
        pass

    elif (month != None) and (year == None):
        print("month given, no year")
        pass

    url = (f"https://www.eia.gov/electricity/data/eia860m/archive/xls/"+
           f"{m}_generator{y}.xlsx")

    try:
        df = pd.read_excel(url,
                           sheet_name='Operating',
                           skipfooter=2,
                           skiprows=2,
                           usecols=columns,
                           index_col='Entity ID')
    except:
        try:
            df = pd.read_excel(url,
                               sheet_name='Operating',
                               skipfooter=2,
                               skiprows=1,
                               usecols=columns,
                               index_col='Entity ID')
        except:
            from pygenesys.data.library import eia_electric_generators
            df = pd.read_excel(eia_electric_generators,
                               sheet_name='Operating',
                               skipfooter=2,
                               skiprows=2,
                               usecols=columns,
                               index_col='Entity ID')

    return df

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
        The dataframe for eia form 860m
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

    # verify the technology string is well formed
    technology = technology.split(' ')
    technology = [i.capitalize() for i in technology]
    technology = ' '.join(technology)

    # filter by region
    if len(region) == 2:
        region_mask = df['Plant State'] == region.upper()
    else:
        region_mask = df['County'] == region.upper()

    df = df[region_mask]


    # filter by technology
    tech_mask = df['Technology'] == technology
    try:
        tech_df = df[tech_mask]
    except:
        print("Technology does not exist within specified region")
        return {}
    # columns = ['Nameplate Capactiy (MW)', 'Operating Year', 'Technology', '']
    # breakpoint()
    sorted_tech_df = tech_df.sort_values(by=['Operating Year'])
    sorted_tech_df.set_index('Operating Year', inplace=True)
    sorted_tech_df.index = pd.to_datetime(sorted_tech_df.index, format='%Y')
    sorted_tech_df = sorted_tech_df.resample('Y').sum()


    existing_years = np.array(sorted_tech_df.index.year).astype('int')
    existing_cap = np.array(sorted_tech_df['Nameplate Capacity (MW)'])

    existing_capacity = {}
    years = []
    caps = []
    for y, c in zip(existing_years, existing_cap):
        if c > 0.0:
            years.append(y)
            caps.append(c)


    return dict(zip(years, caps))


if __name__=='__main__':
    eia_data = get_eia_generators()
    my_dict = get_existing_capacity(eia_data, region='IL', technology='Nuclear')
    print(my_dict)
