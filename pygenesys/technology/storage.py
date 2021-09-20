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
