import numpy as np


def choose_method(method_name='linear'):
    """
    This function returns a function that calculates the growth of
    some quantity.

    Parameters
    ----------
    method_name : string
        The name of the growth method. Accepts: linear
        TODO: add logistic.
    """

    method = {
        'linear':linear_growth,
        'exponential':exponential_growth
    }

    return method[method_name]


def linear_growth(init_value, start_year, end_year, N_years, growth_rate):
    """
    This function returns a numpy array representing the growth
    of a quantity in each given year. Use this function if the growth
    is expected to be linear.

    Parameters
    ----------
    init_value : float
        The initial value value
    start_year : integer
        The first year of the simulation
    end_year : integer
        The last year of the simulation
    N_years : integer
        The number of years simulated between ``start_year`` and
        ``end_year``.
    growth_rate : float
        The rate of growth for the given quantity.

    Returns
    -------
    growth_data : numpy array
        An array of the value for each year in a simulation.
    """

    model = lambda x, init_val, start, rate: rate*init_val*(x-start) + init_val
    years = np.linspace(start_year, end_year, N_years).astype('int')
    growth_data = model(years, init_value, start_year, growth_rate)

    return growth_data


def exponential_growth(init_value, start_year, end_year, N_years, growth_rate):
    """
    This function returns a numpy array representing the growth
    of a quantity in each given year. Use this function if the growth
    is expected to be linear.

    Parameters
    ----------
    init_value : float
        The initial value value
    start_year : integer
        The first year of the simulation
    end_year : integer
        The last year of the simulation
    N_years : integer
        The number of years simulated between ``start_year`` and
        ``end_year``.
    growth_rate : float
        The rate of growth for the given quantity.

    Returns
    -------
    growth_data : numpy array
        An array of the value for each year in a simulation.
    """

    model = lambda x, init_val, start, rate: init_val*np.exp(rate*(x-start))
    years = np.linspace(start_year, end_year, N_years).astype('int')
    growth_data = model(years, init_value, start_year, growth_rate)

    return growth_data

# TODO finish implementing logistic growth
def logistic_growth(init_value, start_year, end_year, N_years, growth_rate, cap):
    """
    This function returns a numpy array representing the growth
    of a quantity in each given year. Use this function if the growth
    is expected to be linear.

    Parameters
    ----------
    init_value : float
        The initial value value
    start_year : integer
        The first year of the simulation
    end_year : integer
        The last year of the simulation
    N_years : integer
        The number of years simulated between ``start_year`` and
        ``end_year``.
    growth_rate : float
        The rate of growth for the given quantity.

    cap : float
        The "carrying capacity" for a given quantity. I.e. the maximum
        sustainable value.

    Returns
    -------
    growth_data : numpy array
        An array of the value for each year in a simulation.
    """

    # model = lambda x, init_val, start, rate: init_val*np.exp(rate*(x-start))
    years = np.linspace(start_year, end_year, N_years).astype('int')
    growth_data = model(years, init_value, start_year, growth_rate)

    return growth_data
