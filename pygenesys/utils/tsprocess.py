import numpy as np
import pandas as pd


def choose_distribution_method(N_seasons, N_hours):
    """
    This function returns a function that appropriately calculates
    the distribution based on the specified time slices. In the
    future, there may be a way to make this more generic.

    Parameters
    ----------
    data_path : string
        The path to the data. It should be a .csv file.
    N_seasons : integer
        The number of seasons in the energy system model.
    N_hours : integer
        The hourly resolution of the energy system model.

    Returns
    -------
    distribution_func : function
        The function to generate a specific distribution of data.
    """
    distribution_func = None

    if (N_seasons == 4) and (N_hours == 24):
        distribution_func = four_seasons_hourly
    elif (N_seasons==12) and (N_hours==24):
        distribution_func = monthly_hourly
    elif (N_seasons == 365) and (N_hours == 24):
        distribution_func = daily_hourly
    return distribution_func


def four_seasons_hourly(data_path, N_seasons=4, N_hours=24, kind='demand'):
    """
    This function calculates a seasonal trend based on the
    input data. Answers the question: what fraction of the annual
    demand is consumed at this time of the year?

    Parameters
    ----------
    data_path : string
        The path to the time series data
            * must be a ``.csv`` file
            * nust have a column ``time`` that is a pandas datetime column
        Tips:
            * Sometimes a dataset will have an index column that can
              be read as an ``Unnamed Column: 0``. If a user supplies
              their own data, this should be removed where applicable.
    kind : string
        The string representing the kind of profile we're interested in.
        Accepts: 'CF', 'cf', 'demand', 'Demand', 'DEMAND'
            'CF' : A capacity factor profile is returned (sum != 1).
            'Demand': Returns a demand profile (sum = 1)
    N_seasons : integer
        The number of seasons in the energy system model.
    N_hours : integer
        The hourly resolution of the energy system model.

    Returns
    -------
    distribution : numpy array
        The time series data distributed over the specified time
        slices.
    """
    time_series = pd.read_csv(data_path,
                              usecols=[0, 1],
                              index_col=['time'],
                              parse_dates=True,
                              )

    # assumes northern latitudes
    spring_mask = ((time_series.index.month >= 3) &
                   (time_series.index.month <= 5))
    summer_mask = ((time_series.index.month >= 6) &
                   (time_series.index.month <= 8))
    fall_mask = ((time_series.index.month >= 9) &
                 (time_series.index.month <= 11))
    winter_mask = ((time_series.index.month == 12) |
                   (time_series.index.month == 1) |
                   (time_series.index.month == 2))

    seasons = {'spring': spring_mask,
               'summer': summer_mask,
               'fall': fall_mask,
               'winter': winter_mask}

    # initialize dictionary
    seasonal_hourly_profile = np.zeros((N_seasons, N_hours))
    for i, season in enumerate(seasons):
        mask = seasons[season]
        season_df = time_series[mask]
        hours_grouped = season_df.groupby(season_df.index.hour)

        avg_hourly = np.zeros(len(hours_grouped))
        std_hourly = np.zeros(len(hours_grouped))
        for j, hour in enumerate(hours_grouped.groups):
            hour_data = hours_grouped.get_group(hour)
            avg_hourly[j] = hour_data.iloc[:, 0].mean()
            std_hourly[j] = hour_data.iloc[:, 0].std()

        if kind.lower() == "demand":
            data = (avg_hourly / (N_seasons * avg_hourly.sum()))
        elif kind.lower() == "cf":
            data = (avg_hourly / (time_series.iloc[:, 0].max()))

        seasonal_hourly_profile[i] = data

    return seasonal_hourly_profile


def monthly_hourly(data_path, N_seasons=12, N_hours=24, kind='demand'):
    """
    This function calculates a seasonal trend based on the
    input data. Answers the question: what fraction of the annual
    demand is consumed at this time of the year?

    Parameters
    ----------
    data_path : string
        The path to the time series data
            * must be a ``.csv`` file
            * nust have a column ``time`` that is a pandas datetime column
        Tips:
            * Sometimes a dataset will have an index column that can
              be read as an ``Unnamed Column: 0``. If a user supplies
              their own data, this should be removed where applicable.
    kind : string
        The string representing the kind of profile we're interested in.
        Accepts: 'CF', 'cf', 'demand', 'Demand', 'DEMAND'
            'CF' : A capacity factor profile is returned (sum != 1).
            'Demand': Returns a demand profile (sum = 1)
    N_seasons : integer
        The number of seasons in the energy system model.
    N_hours : integer
        The hourly resolution of the energy system model.

    Returns
    -------
    distribution : numpy array
        The time series data distributed over the specified time
        slices.
    """
    time_series = pd.read_csv(data_path,
                              usecols=[0, 1],
                              index_col=['time'],
                              parse_dates=True,
                              )

    # initialize dictionary

    months_grouped = time_series.groupby(time_series.index.month)

    monthly_hourly_profile = np.zeros((N_seasons, N_hours))
    for i, month in enumerate(months_grouped.groups):
        month_df = months_grouped.get_group(month)
        hours_grouped = month_df.groupby(month_df.index.hour)

        avg_hourly = np.zeros(len(hours_grouped))
        std_hourly = np.zeros(len(hours_grouped))
        for j, hour in enumerate(hours_grouped.groups):
            hour_data = hours_grouped.get_group(hour)
            avg_hourly[j] = hour_data.iloc[:, 0].mean()
            std_hourly[j] = hour_data.iloc[:, 0].std()

        if kind.lower() == "demand":
            data = (avg_hourly / (N_seasons * avg_hourly.sum()))
        elif kind.lower() == "cf":
            data = (avg_hourly / (time_series.iloc[:, 0].max()))

        monthly_hourly_profile[i] = data

    return monthly_hourly_profile


def daily_hourly(data_path, N_seasons=365, N_hours=24, kind='demand'):
    """
    This function calculates a seasonal trend based on the
    input data. Answers the question: what fraction of the annual
    demand is consumed at this time of the year?

    Parameters
    ----------
    data_path : string
        The path to the time series data
            * must be a ``.csv`` file
            * must have a column ``time`` that is a pandas datetime column
        Tips:
            * Sometimes a dataset will have an index column that can
              be read as an ``Unnamed Column: 0``. If a user supplies
              their own data, this should be removed where applicable.

    N_seasons : integer
        The number of seasons in the energy system model.
    N_hours : integer
        The hourly resolution of the energy system model.

    Returns
    -------
    distribution : numpy array
        The time series data distributed over the specified time
        slices.
    """
    try:
        time_series = pd.read_csv(data_path,
                                  usecols=[0, 1],
                                  index_col=['time'],
                                  parse_dates=True,
                                  )
    except BaseException:
        except_string = """
                        Could not import time series data. Check the following:

                        1. That the path to the file is correct.
                        2. The dataset has two columns: "time" and a column
                           with your data.
                        3. The "time" column has a pandas datetime index.
                        """
        print(except_string)

    time_series = time_series.resample('H').mean()
    time_series.interpolate('linear', inplace=True)
    years_grouped = time_series.groupby(time_series.index.year)
    data_list = []
    for year in years_grouped.groups:
        data = years_grouped.get_group(year)
        if len(data) >= 8760:
            data_list.append(np.array(data.iloc[:, 0])[:8760])
        else:
            pass
            # data_list.append(np.array(data.iloc[:, 0]))
    data_list = np.array(data_list)
    average_profile = data_list.mean(axis=0)
    if kind.lower() == "demand":
        daily_hourly_profile = average_profile / average_profile.sum()
    elif kind.lower() == "cf":
        daily_hourly_profile = (
            average_profile / (time_series.iloc[:, 0].max()))
    return daily_hourly_profile


if __name__ == '__main__':

    from pygenesys.data.library import campus_stm_demand, campus_elc_demand
    from pygenesys.data.library import railsplitter_data, solarfarm_data
    import matplotlib.pyplot as plt
    plt.style.use('ggplot')

    seasons = {0: 'spring',
               1: 'summer',
               2: 'fall',
               3: 'winter'}

    months_list = ['January', 'February', 'March', 'April','May', 'June',
                   'July', 'August', 'September','October','November','December']

    months = dict(enumerate(months_list))
    print(months)

    N_seasons = 12
    N_hours = 24
    method = choose_distribution_method(N_seasons, N_hours)
    # profile = method(railsplitter_data, kind='cf')
    profile = method(campus_elc_demand, kind='demand')
    print(profile.sum())
    for i in range(N_seasons):
        plt.plot(range(N_hours),
                 profile[i],
                 label=f'{months[i].capitalize()}',
                 marker='.')
    # plt.scatter(range(N_hours*N_seasons),
    #          profile,
    #          marker='.')
    # plt.plot(profile)
    plt.legend()
    plt.show()
    # print(len(profile))
