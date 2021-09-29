"""
This file contains information for pre-made transmission technologies. These
technologies do not generate anything, they simply transport energy from one
pool to another.

E.g. you might have several technologies that produce electricity and some
other technologies that *use* electricity upstream while also having an
electricity *demand.* In this case, a transmission technology is useful to
carry energy from the source to the final demand.

Possible confusion:
    * NUCLEAR_ELC produces electricity and is written in this file.
    * NUCLEAR_THM produces thermal energy (e.g. steam) and is written in
      another file, ``thermal.py``.
"""

from pygenesys.technology.technology import Technology

STM_TUNNEL = Technology(tech_name='STM_TUNNEL',
                        units='MW(th)',
                        tech_sector='transmission',
                        tech_label='p',
                        description='steam tunnels for district heating',
                        category='steam',
                        capacity_to_activity=1.00,)
TRANSMISSION = Technology(tech_name='TRANSMISSION',
                          units='MWe',
                          tech_sector='transmission',
                          tech_label='p',
                          description='electric transmission lines',
                          category='electricity',
                          capacity_to_activity=1.00,)
CW_PIPES = Technology(tech_name='CW_PIPES',
                      units='million ton-hours',
                      tech_sector='transmission',
                      tech_label='p',
                      description='chilled water',
                      category='transmission',
                      capacity_to_activity=1.00,)

if __name__ == "__main__":

    print(help(Technology))
