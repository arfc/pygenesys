import numpy as np
import pandas as pd
import datetime as dt



def timeseries_preprocess(ts):
    """
    This function preprocesses data ensuring there
    are no NaN values and no missing hours.
    """

    time_series = ts.copy()
    time_series = time_series.resample('H').mean()
    time_series.interpolate('linear', inplace=True)

    start = time_series.index.date[0]
    end = time_series.tail(1).index[0]

    idx_name = time_series.index.name

    indx_df = pd.DataFrame({idx_name:pd.date_range(start, end, freq='H')})
    indx_df.set_index(idx_name, inplace=True)
    time_series = pd.concat([indx_df,
                             time_series],
                             axis=1).interpolate('linear').backfill()

    return time_series



def load_duration_curve(df):
    """
    Returns the load duration curve data
    """

    data = np.array(df.iloc[:,0])
    sorted_data = np.sort(data)[::-1]
    pct = np.linspace(0,100, len(sorted_data))

    return pct, sorted_data


def get_peak_day(dataframe):
    """
    This function retrieves the peak day for a given timeseries.
    """

    time_series = dataframe.copy()
    idx = time_series.where(time_series == time_series.max()).dropna().index.date[0]
    idx_delta = idx + dt.timedelta(days=1)
    peak_day = time_series[idx:idx_delta][:24]

    return peak_day


def get_weekends(dataframe):
    """
    This function retrieves the peak day for a given timeseries.
    """

    time_series = dataframe.copy()
    weekend_mask = (time_series.index.weekday==5) | (time_series.index.weekday==6)
    weekends = time_series[weekend_mask]
    weekend_hourly = weekends.groupby(weekends.index.hour).mean()[:24]

    return weekend_hourly


def get_season_masks(df):
    """
    Returns seasonal masks for given timeseries.
    """
    spring_mask = ((df.index.month >= 3) & (df.index.month <= 5))
    summer_mask = ((df.index.month >= 6) & (df.index.month <= 8))
    fall_mask = ((df.index.month >= 9) & (df.index.month <= 11))
    winter_mask = ((df.index.month == 12) | (df.index.month == 1) |
                   (df.index.month == 2))

    seasons = {'spring': spring_mask,
               'summer': summer_mask,
               'fall': fall_mask,
               'winter': winter_mask}

    return seasons


def four_seasons_hourly(dataframe,
                        N_seasons=4,
                        N_hours=24,
                        kind='demand',
                        add_peak=False,
                        add_weekend=False,
                        how=None, N_segments=1):
    """
    This function calculates a seasonal trend based on the
    input data. Answers the question: what fraction of the annual
    demand is consumed at this time of the year?

    Parameters
    ----------
    dataframe : string, or pandas dataframe
        The path to the time series data or a pandas dataframe
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
    how : string
        The time series aggregation method. Only used in ``tsprocess.create_timeslices``
        which depends on the ``tsam`` package.

    Returns
    -------
    distribution : numpy array
        The time series data distributed over the specified time
        slices.
    """
    if isinstance(dataframe, str):
        time_series = pd.read_csv(dataframe,
                                  usecols=[0, 1],
                                  index_col=['time'],
                                  parse_dates=True,
                                  )
    elif isinstance(dataframe, pd.DataFrame):
        time_series = dataframe

    # assumes northern latitudes
    seasons = get_season_masks(time_series)

    seasonal_hourly_profile = np.zeros((N_seasons,N_hours))
    for i, season in enumerate(list(seasons.values())):
        season_df = time_series[season]
        idx = int(N_segments*i)
        seasonal_hourly_profile[idx] = season_df.groupby(season_df.index.hour).mean().values.reshape((24,))

        if add_peak:
            idx += 1
            peak_day = get_peak_day(season_df).values.reshape((24,))
            seasonal_hourly_profile[idx] = peak_day

        if add_weekend:
            idx += 1
            weekend = get_weekends(season_df).values.reshape((24,))
            seasonal_hourly_profile[idx] = weekend

    if kind.lower() == "demand":
        seasonal_hourly_profile = (seasonal_hourly_profile / (seasonal_hourly_profile.sum()))
    elif kind.lower() == "cf":
        seasonal_hourly_profile = (seasonal_hourly_profile / (time_series.iloc[:, 0].max()))

    return seasonal_hourly_profile


def aggregate(dataframe,
              N_seasons=4,
              N_hours=24,
              kind='demand',
              groupby='season',
              add_peak=False,
              add_weekend=False,
              how=None):
    """
    This function calculates a seasonal trend based on the
    input data. Answers the question: what fraction of the annual
    demand is consumed at this time of the year?

    Parameters
    ----------
    dataframe : string, or pandas dataframe
        The path to the time series data or a pandas dataframe
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
    groupby : string
        Indicates how the time series should be grouped.
        Accepts:
            * season : data will be grouped by seasons.
            * month : data will be grouped by months.
            * week : data will be grouped by week of year.
            * day : data will be grouped by day of year.
    N_seasons : integer
        The number of seasons in the energy system model.
    N_hours : integer
        The hourly resolution of the energy system model.
    how : string
        The time series aggregation method. Only used in ``tsprocess.create_timeslices``
        which depends on the ``tsam`` package.
    add_peak : boolean
        Indicates whether desired time slices include peak days.
    add_weekend : boolean
        Indicates whether desired time slices include weekends.

    Returns
    -------
    distribution : numpy array
        The time series data distributed over the specified time
        slices.
    """
    # read in the data
    if isinstance(dataframe, str):
        time_series = pd.read_csv(dataframe,
                                  usecols=[0, 1],
                                  index_col=['time'],
                                  parse_dates=True,
                                  )
    elif isinstance(dataframe, pd.DataFrame):
        time_series = dataframe

    time_series = timeseries_preprocess(time_series)

    # how many period segments to calculate
    N_segments = 1 + int(add_peak) + int(add_weekend)


    N_per_year = {'season':4,
                  'month':12,
                  'week':52,
                  'day':365}
    #
    # if int(N_seasons/N_segments) < N_per_year[groupby]:
    #     raise Exception(f"Not enough seasons in model. Change N_seasons to {N_per_year[groupby]*N_segments}")

    hourly_profiles = np.zeros((N_seasons, N_hours))

    # group the time series
    if groupby == 'season':
        hourly_profiles = four_seasons_hourly(dataframe,
                                              N_seasons=N_seasons,
                                              N_hours=N_hours,
                                              kind=kind,
                                              add_peak=add_peak,
                                              add_weekend=add_weekend,
                                              N_segments=N_segments)
        return hourly_profiles

    # all other cases
    elif groupby == 'month':
        grouped = time_series.groupby(time_series.index.month)
    elif groupby == 'week':
        grouped = time_series.groupby(time_series.index.isocalendar().week)
    elif groupby == 'day':
        grouped = time_series.groupby(time_series.index.dayofyear)
    # initialize dictionary
    for i, group in enumerate(grouped.groups):
        if (group > 52) and (groupby=='week'):
            continue
        elif (group > 365) and (groupby=='day'):
            continue
        group_df = grouped.get_group(group)

        idx = int(N_segments*i)
        hourly_profiles[idx] = group_df.groupby(group_df.index.hour).mean().values.reshape((24,))

        if add_peak:
            idx += 1
            peak_day = get_peak_day(group_df).values.reshape((24,))
            hourly_profiles[idx] = peak_day

        if add_weekend:
            idx += 1
            weekend = get_weekends(group_df).values.reshape((24,))
            hourly_profiles[idx] = weekend


    if kind.lower() == "demand":
        hourly_profiles = (hourly_profiles / (hourly_profiles.sum()))
    elif kind.lower() == "cf":
        hourly_profiles = (hourly_profiles / (time_series.iloc[:, 0].max()))


    return hourly_profiles


def create_timeslices(dataframe, normalize=None, n_seasons=4, n_hours=24, how='averaging'):
    """
    This function calculates representative time slices based on the
    input data. Answers the question: what fraction of the annual
    demand is consumed at this time of the year?

    Parameters
    ----------
    dataframe : string or pandas.DataFrame
        The path to the time series data
            * must be a ``.csv`` file
            * must have a column ``time`` that is a pandas datetime column
        Tips:
            * Sometimes a dataset will have an index column that can
              be read as an ``Unnamed Column: 0``. If a user supplies
              their own data, this should be removed where applicable.
    normalize : string
        Indicates the type of normalization. Accepts "demand" and "cf."
            * "demand" normalizes by the sum of the aggregated data. The resultant
            sum is unity (i.e. the l-1 norm).
            * "cf" normalizes by the maximum value of the aggregated data (i.e.
            the infinity norm)
    N_seasons : integer
        The number of seasons in the energy system model.
    N_hours : integer
        The hourly resolution of the energy system model.
    how : string
        The time series aggregation method. Only used in ``tsprocess.create_timeslices``
        which depends on the ``tsam`` package.

    Returns
    -------
    distribution : numpy array
        The time series data distributed over the specified time
        slices.
    """

    if isinstance(dataframe, str):
        time_series = pd.read_csv(dataframe,
                                  usecols=[0, 1],
                                  index_col=['time'],
                                  parse_dates=True,
                                  )
    elif isinstance(dataframe, pd.DataFrame):
        time_series = dataframe

    aggregation = tsam.TimeSeriesAggregation(time_series,
                                             noTypicalPeriods=n_seasons,
                                             hoursPerPeriod=24,
                                             clusterMethod=how)

    typPeriods = aggregation.createTypicalPeriods()

    if normalize == 'demand':
        sum_val = typPeriods.iloc[:,0].sum()
        typPeriods.iloc[:,0] = typPeriods.iloc[:,0]/sum_val

    elif normalize == 'cf':
        max_val = typPeriods.iloc[:,0].max()
        typPeriods.iloc[:,0] = typPeriods.iloc[:,0]/max_val

    profile = typPeriods.iloc[:,0].values

    return profile


if __name__ == '__main__':

    from pygenesys.data.library import campus_stm_demand, campus_elc_demand
    from pygenesys.data.library import railsplitter_data, solarfarm_data
    import matplotlib.pyplot as plt
