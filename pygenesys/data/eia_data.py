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

    return month, day, int(year)


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

    # initialize 
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
    except BaseException:
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


if __name__ == '__main__':
    eia_data = get_eia_generators()
    my_dict = get_existing_capacity(
        eia_data, region='IL', technology='Nuclear')
    print(my_dict)
