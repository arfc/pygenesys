import pygenesys.utils.growth_model as pyutgm
from pytest import approx
import numpy as np


def test_choose_growth_method_no_imput():
    linear = pyutgm.choose_growth_method()
    if str(linear).find("linear_growth") != -1:
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
    growth = pyutgm.linear_growth(init_value,
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
    growth = pyutgm.exponential_growth(init_value,
                                    start_year,
                                    end_year,
                                    N_years,
                                    growth_rate)

    assert(growth == approx(np.array([1., 2.71828183])))

    return


def test_logistic_growth_unit():
    """
    Test logistic growth over one step
    for a unit growth rate. With a carrying
    capacity smaller than pure exponential
    growth would exhibit.
    """

    init_value = 1
    start_year = 1
    end_year = 2
    N_years = 2
    growth_rate = 1
    cap = 2
    growth = pyutgm.logistic_growth(init_value,
                                    start_year,
                                    end_year,
                                    N_years,
                                    growth_rate,
                                    cap)

    assert(growth == approx(np.array([1,
                                        1.4621171572600098,
                                        1.7615941559557646])))

    return
