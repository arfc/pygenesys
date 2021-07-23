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

uranium_ntl = Commodity(comm_name='uranium_ntl',
                        units='tonnes',
                        description='natural uranium -- infinite reservoir')

ethos = Commodity(comm_name='ethos',
                  units='NULL',
                  description='placeholder commodity -- infinite reservoir')
