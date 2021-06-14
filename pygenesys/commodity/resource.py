from pygenesys.commodity.commodity import Commodity

electricity = Commodity(comm_name='ELC',
                        units = 'GWh',
                        description = 'Electricity')

steam = Commodity(comm_name='STM',
                  units = 'GWh(th)',
                  description = 'Steam')

ethos = Commodity(comm_name='ethos',
                  units='NULL',
                  description='placeholder commodity -- infinite reservoir')                
