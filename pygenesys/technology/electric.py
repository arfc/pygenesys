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


SOLAR_FARM = Technology(tech_name='SOLAR_FARM',
                        units="MWe",
                        tech_sector='electricity',
                        tech_label='p',
                        description='utility scale solar',
                        category='solar',
                        capacity_to_activity=8.76,
                        )
