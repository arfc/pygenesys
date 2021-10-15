"""
This file contains information for pre-made electricity production
technologies. These technologies generate electricity as the primary energy
carrier.

Possible confusion:
    * NUCLEAR_ELC produces electricity and is written in this file.
    * NUCLEAR_THM produces thermal energy (e.g. steam) and is written in
      another file, ``thermal.py``.
"""

from pygenesys.technology.technology import Technology

NUCLEAR_ELC = Technology(tech_name='NUCLEAR_ELC',
                         units="MWe",
                         tech_sector='electricity',
                         tech_label='pb',
                         description='nuclear power plant',
                         category='uranium',
                         capacity_to_activity=8.76,
                         )

NUCLEAR_TB = Technology(tech_name='NUCLEAR_TB',
                        units="MWe",
                        tech_sector='electricity',
                        tech_label='p',
                        description='nuclear steam turbine',
                        category='electric',
                        capacity_to_activity=8.76,)

NUCLEAR_CONV = Technology(tech_name='NUCLEAR_CONV',
                         units="MWe",
                         tech_sector='electricity',
                         tech_label='pb',
                         description='conventional nuclear plant',
                         category='uranium',
                         capacity_to_activity=8.76,
                         ramping_tech=False,
                         )

NUCLEAR_ADV = Technology(tech_name='NUCLEAR_ADV',
                         units="MWe",
                         tech_sector='electricity',
                         tech_label='p',
                         description='advanced nuclear plant',
                         category='uranium',
                         capacity_to_activity=8.76,
                         ramping_tech=True
                         )

COAL_CONV = Technology(tech_name='COAL_CONV',
                      units="MWth",
                      tech_sector='electricity',
                      tech_label='p',
                      description='conventional coal power plant',
                      category='coal',
                      capacity_to_activity=8.76,
                      reserve_tech=True,
                      ramping_tech=True,)


NATGAS_CONV = Technology(tech_name='NATGAS_CONV',
                        units="MWe",
                        tech_sector='electricity',
                        tech_label='p',
                        description='conventional combined cycle natural gas',
                        category='natural gas',
                        capacity_to_activity=8.76,
                        ramping_tech=True,
                        reserve_tech=True)

COAL_ADV = Technology(tech_name='COAL_ADV',
                      units="MWth",
                      tech_sector='electricity',
                      tech_label='p',
                      description='coal power plant with CCS',
                      category='coal',
                      capacity_to_activity=8.76,
                      reserve_tech=True,
                      ramping_tech=True,)


NATGAS_ADV = Technology(tech_name='NATGAS_ADV',
                        units="MWe",
                        tech_sector='electricity',
                        tech_label='p',
                        description='combined cycle natural gas with CCS',
                        category='natural gas',
                        capacity_to_activity=8.76,
                        ramping_tech=True,
                        reserve_tech=True)


ABBOTT_TB = Technology(tech_name='ABBOTT_TB',
                       units="MWe",
                       tech_sector='electricity',
                       tech_label='p',
                       description='abbott steam turbine, UIUC',
                       category='electric',
                       capacity_to_activity=8.76,)


SOLAR_FARM = Technology(tech_name='SOLAR_FARM',
                        units="MWe",
                        tech_sector='electricity',
                        tech_label='p',
                        description='utility scale solar',
                        category='renewable',
                        capacity_to_activity=8.76,
                        curtailed_tech=True)


WIND_FARM = Technology(tech_name='WIND_FARM',
                       units="MWe",
                       tech_sector='electricity',
                       tech_label='p',
                       description='utility scale wind',
                       category='renewable',
                       capacity_to_activity=8.76,
                       curtailed_tech=True,
                       )

IMP_ELC = Technology(tech_name='IMP_ELC',
                     units="MWe",
                     tech_sector='electricity',
                     tech_label='p',
                     description='electricity imports',
                     category='imported',
                     capacity_to_activity=8.76,
                     )
