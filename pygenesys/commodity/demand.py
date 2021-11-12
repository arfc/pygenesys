"""
This file contains pre-defined demand commodities.
"""

from pygenesys.commodity.commodity import DemandCommodity


ELC_DEMAND = DemandCommodity(comm_name='ELC_DEMAND',
                             comm_label='d',
                             units='GWh',
                             description='End-use electricity demand')

STM_DEMAND = DemandCommodity(comm_name='STM_DEMAND',
                             units='GWh(th)',
                             description='End-use steam demand')

CW_DEMAND = DemandCommodity(comm_name='CW_DEMAND',
                            units='Million ton-hours refrigeration',
                            description='End-use chilled water demand')

TRANSPORT = DemandCommodity(comm_name='TRANSPORT',
                            units='thousand gallon gasoline equivalent',
                            description='transportation demand')


if __name__ == '__main__':
    print(ELC_DEMAND._db_entry())
    print(ELC_DEMAND.demand)
    print(STM_DEMAND._db_entry())
