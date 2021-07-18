from pygenesys.commodity.commodity import Commodity

electricity = Commodity(comm_name='ELC',
                        units='GWh',
                        description='Electricity')

steam = Commodity(comm_name='STM',
                  units='GWh(th)',
                  description='Steam')

natural_gas = Commodity(comm_name='NATGAS',
                        units='MMBTU',
                        description='natural gas')

ethos = Commodity(comm_name='ethos',
                  units='NULL',
                  description='placeholder commodity -- infinite reservoir')
