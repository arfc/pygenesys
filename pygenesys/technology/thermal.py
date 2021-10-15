"""
This file contains information for pre-made thermal energy production
technologies.These technologies generate thermal energy as the primary energy
carrier.

Possible confusion:
      * NUCLEAR_THM produces thermal energy (e.g. steam) and is written in
        this file.
      * NUCLEAR_ELC produces electricity and is written in another file,
        ``electric.py``.
"""

from pygenesys.technology.technology import Technology


NUCLEAR_THM = Technology(tech_name='NUCLEAR_THM',
                         units="MWth",
                         tech_sector='thermal',
                         tech_label='p',
                         description='nuclear power plant (thermal)',
                         category='uranium',
                         capacity_to_activity=8.76,
                         reserve_tech=True,
                         ramping_tech=True,)

ABBOTT = Technology(tech_name='ABBOTT',
                    units="MWth",
                    tech_sector='thermal',
                    tech_label='pb',
                    description='natural gas plant',
                    category='natural gas',
                    capacity_to_activity=8.76,
                    reserve_tech=True,
                    ramping_tech=False,)   # change this back to True

CWS = Technology(tech_name='CWS',
                 units="tons of refrigeration",
                 tech_sector='chilled water',
                 tech_label='p',
                 description='electric water chillers',
                 category='chilled water',
                 capacity_to_activity=0.00876,
                 ramping_tech=True,)
