from pygenesys.commodity.commodity import Commodity

electricity = Commodity(comm_name='ELC',
                        units='GWh',
                        description='Electricity')

steam = Commodity(comm_name='STM',
                  units='GWh(th)',
                  description='Steam')
