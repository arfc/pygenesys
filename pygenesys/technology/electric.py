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
                         reserve_tech=True,
                         ramping_tech=True,)

NUCLEAR_TB = Technology(tech_name='NUCLEAR_TB',
                         units="MWe",
                         tech_sector='electricity',
                         tech_label='p',
                         description='nuclear steam turbine',
                         category='electric',
                         capacity_to_activity=8.76,
                         reserve_tech=True,
                         ramping_tech=True,)

ABBOTT_TB = Technology(tech_name='ABBOTT_TB',
                       units="MWe",
                       tech_sector='electricity',
                       tech_label='p',
                       description='abbott steam turbine, UIUC',
                       category='electric',
                       capacity_to_activity=8.76,
                       reserve_tech=True,
                       ramping_tech=True,)


SOLAR_FARM = Technology(tech_name='SOLAR_FARM',
                        units="MWe",
                        tech_sector='electricity',
                        tech_label='p',
                        description='utility scale solar',
                        category='renewable',
                        capacity_to_activity=8.76,
                        )

WIND_FARM = Technology(tech_name='WIND_FARM',
                        units="MWe",
                        tech_sector='electricity',
                        tech_label='p',
                        description='utility scale wind',
                        category='renewable',
                        capacity_to_activity=8.76,
                        )

IMP_ELC = Technology(tech_name='IMP_ELC',
                     units="MWe",
                     tech_sector='electricity',
                     tech_label='p',
                     description='electricity imports',
                     category='imported',
                     capacity_to_activity=8.76,
                     )
