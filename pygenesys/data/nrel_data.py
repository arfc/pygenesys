from pygenesys.data.library import nrel_electric_costs
import pandas as pd
import numpy as np


renewable_techs = ['LandbasedWind',
                   'OffshoreWind',
                   'UtilityPV',
                   'ResPV',
                   'CommPV',
                   'Geothermal',
                   'Hydropower',
                   'CSP',]


def read_atb_data(atb_year=2021):
    """
    This function returns the NREL Annual Technology
    Baseline (ATB) data as a pandas dataframe. Reads
    from ``pygenesys.data.library``

    Parameters
    ----------
    atb_year : integer
        Indicates the ATB version. Default is 2021.
    """

    df = pd.read_csv(nrel_electric_costs,
                     usecols=['atb_year',
                              'core_metric_parameter',
                              'core_metric_case',
                              'technology',
                              'techdetail',
                              'scenario',
                              'core_metric_variable',
                              'value'],)

    df.dropna(axis=1, inplace=True)
    df.rename(columns={'core_metric_variable':'year'}, inplace=True)
    df.set_index('year', inplace=True)

    df = df[df['atb_year']==atb_year]

    df = df.drop('atb_year', axis=1)

    return df


def return_nrel_scenario(df, scenario):
    """
    This function returns an ATB dataframe for only one
    scenario.

    Parameters
    ----------
    df : Pandas DataFrame
        The NREL ATB dataframe. Must have a ``scenario`` column
        with values ['Advanced','Conservative', 'Moderate'].
    scenario : string
        Specifies the scenario of interest. Must be
        * Advanced
        * Conservative
        * Moderate
    """

    df = df[df['scenario'] == scenario]

    return df


def get_nrel_techs(df):
    """
    Returns the names of the technologyies in
    the NREL ATB.
    """

    tech_list = np.unique(df['technology'])

    return tech_list

def nrel_cost_projection(tech,
                         cost_metric,
                         tech_detail=None,
                         scenario='Moderate',):
    """
    Returns cost projections from the NREL Annual
    Technology Baseline.

    Parameters
    ----------
    tech : string
        The name of the technology in the NREL ATB.
        Accepted keys:
        * 'Commercial Battery Storage' : Li-ion battery storage
        * 'Utility-scale Battery Storage' : Li-ion battery storage
        * 'Residential Battery Storage' : Li-ion battery storage
        * 'Biopower' : Biopower
        * 'CSP' : Concentrated solar power
        * 'Coal_FE' : Coal Fueled Electricity (COAL FE) power plant
        * 'CommPV' : Commercial rooftop PV solar
        * 'Geothermal' : Geothermal electricity
        * 'Hydropower' : Conventional hydropower
        * 'LandbasedWind' : Onshore wind
        * 'NaturalGas_FE' : Natural gas fired power plant
        * 'Nuclear' : Advanced nuclear power (AP1000)
        * 'OffShoreWind' : Offshore wind
        * 'ResPV' : Residential rooftop PV solar
        * 'UtilityPV' : Utility scale PV solar
    cost_metric : string
        The string indicating the cost metric
    """
    return


if __name__ == "__main__":

    df = read_atb_data()
    scenario = 'Conservative'
    df = return_nrel_scenario(df, scenario)
    df = df[df['technology'] == 'Nuclear']
    param = 'CAPEX'
    # param = 'Fixed O&M'
    # param = 'Variable O&M'
    # df = df[df['core_metric_parameter']==param]
    print(df.columns)
    for col in df.columns:
        print(col)
        print(np.unique(df[col]))
    print(df.head(5))
