import pandas as pd
import numpy as np


def nrel_cost_projection(tech,
                         cost_metric,
                         tech_detail=None,
                         scenario='Moderate',
                         atb_year=2020):
    """
    Returns cost projections from the NREL Annual
    Technology Baseline.

    Parameters
    ----------
    tech : string
        The name of the technology in the NREL ATB.
        Accepted keys:
        * 'Battery' : Li-ion battery storage
        * 'Biopower' : Biopower
        * 'CSP' : Concentrated solar power
        * 'Coal' : Coal fired power plant
        * 'CommPV' : Commercial rooftop PV solar
        * 'Geothermal' : Geothermal electricity
        * 'Hydropower' : Conventional hydropower
        * 'LandbasedWind' : Onshore wind
        * 'NaturalGas' : Natural gas fired power plant
        * 'Nuclear' : Conventional nuclear power
        * 'OffShoreWind' : Offshore wind
        * 'ResPV' : Residential rooftop PV solar
        * 'UtilityPV' : Utility scale PV solar
    cost_metric : string
        The string indicating the cost metric
    """
    return
