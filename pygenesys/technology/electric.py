"""
This file contains information for pre-made electricity produciton technologies.
These technologies generate electricity as the primary energy carrier.

Possible confusion:
    * NUCLEAR_ELC produces electricity and is written in this file.
    * NUCLEAR_THM produces thermal energy (e.g. steam) and is written in another
    file, ``thermal.py``.
"""

from pygenesys.technology.technology import Technology

NUCLEAR_ELC = Technology(tech_name='NUCLEAR_ELC',
                         units="MWe",
                         tech_sector='electricity',
                         tech_label='pb',
                         description='nuclear power plant',
                         category='uranium')