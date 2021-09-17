"""
This file contains pre-defined emissions commodities.
"""

from pygenesys.commodity.commodity import EmissionsCommodity


co2eq = EmissionsCommodity(comm_name='co2eq',
                           comm_label='e',
                           units='Mtons',
                           description='gaseous emissions, CO2 equivalent')

if __name__ == "__main__":

    from pygenesys.commodity.commodity import *
    
    import numpy as np

    types = np.array([EmissionsCommodity, DemandCommodity, Commodity])
    print(type(co2eq))
    print(np.any(types == type(co2eq)))
