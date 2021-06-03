"""
This file contains pre-defined demand commodities.
"""

from pygenesys.commodity.commodity import DemandCommodity


ELC_DEMAND = DemandCommodity(comm_name='ELC_DEMAND',
                             comm_label='d',
                             units='GWh',
                             description='End-use electricity demand')


if __name__ == '__main__':
    print(ELC_DEMAND._db_entry())                            
