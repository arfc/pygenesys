from pygenesys.data.eia_data import *
import pytest
from datetime import date
import pandas as pd


def test_get_date():
    """
    Tests the get_date function.
    """

    today = date.today().strftime("%B %d, %Y")

    today = today.split(' ')

    m, d, y = get_date()

    assert m == today[0]
    assert d == today[1]
    assert y == int(today[2])

    return


def test_capitalize_string_case1():
    """
    Tests the capitalize string function with two words.
    """

    expected_string = "Natural Gas"

    assert capitalize_string('natural gas') == expected_string
    assert capitalize_string('Natural gas') == expected_string
    assert capitalize_string('natural Gas') == expected_string
    assert capitalize_string('NATURAL GAS') == expected_string

    return


def test_capitalize_string_case2():
    """
    Tests the capitalize string function with one word.
    """

    expected_string = "Nuclear"

    assert capitalize_string('nuclear') == expected_string
    assert capitalize_string('Nuclear') == expected_string
    assert capitalize_string('NUCLEAR') == expected_string

    return


def test_get_eia_generators_none_passed():
    """
    Tests the data download function where
    neither the month nor year are specified.
    """

    df = get_eia_generators()

    assert isinstance(df, pd.DataFrame)

    return


def test_get_eia_generators_month_passed():
    """
    Tests the data download function where
    only the month is passed.
    """

    with pytest.raises(ValueError):
        df = get_eia_generators(month='January')

    return


def test_get_eia_generators_year_passed():
    """
    Tests the data download function where
    only the year is passed.
    """

    with pytest.raises(ValueError):
        df = get_eia_generators(year=2022)

    return


def test_get_eia_generators_bad_year_month():
    """
    Tests the data download function where
    only the year is passed.
    """
    month = 'thermidor'
    year = 2

    with pytest.raises(ValueError):
        df = get_eia_generators(month=month, year=year)

    return


df = get_eia_generators()


def test_get_region_techs_state():
    """
    Tests the regional filter function using a
    state abbreviation.
    """

    state = 'IL'
    region_techs = get_region_techs(df, region=state)

    assert len(region_techs) > 0

    return


def test_get_region_techs_bad_state():
    """
    Tests the regional filter function using a
    non-existent state abbreviation.
    """

    state = 'QU'
    with pytest.raises(ValueError):
        region_techs = get_region_techs(df, region=state)

    return


def test_get_region_techs_county():
    """
    Tests the regional filter function using a
    county name.
    """

    county = 'Champaign'
    region_techs = get_region_techs(df, region=county)

    assert len(region_techs) > 0

    return


def test_get_region_techs_bad_county():
    """
    Tests the regional filter function using a
    non-existent county name.
    """

    county = 'France'
    with pytest.raises(ValueError):
        region_techs = get_region_techs(df, region=county)

    return


def test_get_tech_good_tech():
    """
    Tests `get_tech`. 
    """
    tech = 'Nuclear'
    tech_df = get_tech(df, technology=tech)

    assert len(tech_df) > 0

    return


def test_get_tech_bad_tech():
    """
    Tests the regional filter function using a
    non-existent state abbreviation.
    """

    tech = 'Dark Matter Combustion Engine'
    with pytest.raises(ValueError):
        tech_df = get_tech(df, technology=tech)

    return


def test_get_existing_capacity_good_tech():
    """
    Tests `get_existing_capacity` with a valid technology.
    """

    tech = 'Nuclear'
    state = 'IL'
    expected_result = {1970: 1009.3,
                       1971: 1009.3,
                       1972: 2018.6,
                       1984: 2340.0,
                       1985: 1224.9,
                       1987: 2363.2,
                       1988: 2449.8}

    assert(get_existing_capacity(df,
                                 region=state,
                                 technology=tech) == expected_result)
