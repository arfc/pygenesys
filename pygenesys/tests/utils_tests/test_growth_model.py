from pygenesys.utils import growth_model
from pytest import approx
import numpy as np


def test_choose_growth_method_no_input():
    linear = growth_model.choose_growth_method()
    if "linear_growth" in str(linear):
        pass
    else:
        raise ValueError("""The wrong function was
                            used by choose_growth_method.""")

    return


def test_linear_growth_unit():
    """
    Test linear growth over one step
    for a unit growth rate.
    """

    init_value = 1
    start_year = 0
    end_year = 1
    N_years = 2
    growth_rate = 1
    growth = growth_model.linear_growth(init_value,
                                        start_year,
                                        end_year,
                                        N_years,
                                        growth_rate)

    assert((growth == np.array([1, 2])).all())

    return


def test_exponential_growth_unit():
    """
    Test exponential growth over one step
    for a unit growth rate.
    """

    init_value = 1
    start_year = 0
    end_year = 1
    N_years = 2
    growth_rate = 1
    growth = growth_model.exponential_growth(init_value,
                                             start_year,
                                             end_year,
                                             N_years,
                                             growth_rate)

    assert(growth == approx(np.array([1., 2.71828183])))

    return


def test_logistic_growth_unit():
    """
    Test logistic growth over two steps
    for a unit growth rate. With a carrying
    capacity smaller than pure exponential
    growth would exhibit.
    """

    init_value = 1
    start_year = 0
    end_year = 2
    N_years = 3
    growth_rate = 1
    cap = 2
    growth = growth_model.logistic_growth(init_value,
                                          start_year,
                                          end_year,
                                          N_years,
                                          growth_rate,
                                          cap)

    assert(growth == approx(np.array([1.,
                                      1.4621171572600098,
                                      1.7615941559557646])))

    return
