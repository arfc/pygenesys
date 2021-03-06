"""
This file contains pre-made commodities.

In practice, any commodity could be an "infinite reservoir" is there is no
technology that "creates" the commodity.
"""

from pygenesys.commodity.commodity import Commodity

electricity = Commodity(comm_name='ELC',
                        units='GWh',
                        description='Electricity')

steam = Commodity(comm_name='STM',
                  units='GWh(th)',
                  description='Steam')

nuclear_steam = Commodity(comm_name='NUC_STM',
                          units='GWh(th)',
                          description='Steam')

chilled_water = Commodity(comm_name='CHW',
                          units='million ton-hours',
                          description='Chilled Water')

natural_gas = Commodity(comm_name='NATGAS',
                        units='MMBTU',
                        description='natural gas')

uranium_leu = Commodity(comm_name='uranium_leu',
                        units='tonnes',
                        description='low enriched uranium')

uranium_ntl = Commodity(comm_name='uranium_ntl',
                        units='tonnes',
                        description='natural uranium -- infinite reservoir')

ethos = Commodity(comm_name='ethos',
                  units='NULL',
                  description='placeholder commodity -- infinite reservoir')
