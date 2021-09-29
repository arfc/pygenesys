"""
This file contains information for pre-made energy storage technologies.
These technologies store energy carrying commodities. For example a "battery"
would store and "produce" electricity.
"""

from pygenesys.technology.technology import Technology

LI_BATTERY = Technology(tech_name='LI_BATTERY',
                        units='MWe',
                        tech_sector='electricity',
                        tech_label='ps',
                        description='lithium ion battery',
                        category='storage',
                        capacity_to_activity=8.76,
                        storage_tech=True)

CW_STORAGE = Technology(tech_name='CW_STORAGE',
                        units='million ton-hours refrigeration',
                        tech_sector='chilled water',
                        tech_label='ps',
                        description='chilled water storage tanks',
                        category='storage',
                        capacity_to_activity=0.00876,
                        storage_tech=True,
                        ramping_tech=True)
