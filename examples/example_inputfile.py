"""
PyGenesys Input File
To run execute:

```bash
genesys --infile example_inputfile.py
```

### Notes

#### Why are there import statements throughout the input file rather than
collected in one place at the top of the file?
---
A fair question, since this is considered "pep8" style. However, the PyGenesys
input file has a different logic from a typical python "module." This input file
should be treated as a workspace with the ultimate purpose of creating an energy
system model. It's unusual to know in-advance every technology and commodity
your energy system will use or require. This example input file respects the
flow of developing an energy sytem rather than enforcing a particular style.

In the end, users will write input files in a way that makes sense to them.
PyGenesys is flexible and will generate a Temoa model as long as the fundamental
pieces are present.
"""
# So the database can be saved in the location from which
# the command is called.
import os
curr_dir = os.path.dirname(__file__)

# Simulation metadata goes here
database_filename = 'my_temoadb.sqlite'  # where the database will be written
scenario_name = 'test'
start_year = 2025  # the first year optimized by the model
end_year = 2050  # the last year optimized by the model
N_years = 6  # the number of years optimized by the model
N_seasons = 4  # the number of "seasons" in the model
N_hours = 24  # the number of hours in a day
reserve_margin = {'IL':0.3}  # fraction of excess capacity to ensure reliability
discount_rate = 0.05  # The discount rate applied globally.

# Import commodities here
from pygenesys.commodity.resource import electricity, steam, ethos, uranium_leu
from pygenesys.commodity.resource import nuclear_steam
from pygenesys.commodity.demand import ELC_DEMAND, STM_DEMAND
from pygenesys.commodity.emissions import co2eq
ELC_DEMAND.add_demand(region='IL',
                      init_demand=183,
                      start_year=start_year,
                      end_year=end_year,
                      N_years=N_years,
                      growth_rate=0.01)
ELC_DEMAND.add_demand(region='UIUC',
                      init_demand=4.44,
                      start_year=start_year,
                      end_year=end_year,
                      N_years=N_years,
                      growth_rate=0.01)
STM_DEMAND.add_demand(region='UIUC',
                      init_demand=6,
                      start_year=start_year,
                      end_year=end_year,
                      N_years=N_years,
                      growth_rate=-0.01,
                      growth_method='exponential')

# Import distribution data
from pygenesys.data.library import campus_elc_demand, campus_stm_demand
ELC_DEMAND.set_distribution(region='UIUC',
                            data=campus_elc_demand,
                            n_seasons=N_seasons,
                            n_hours=N_hours
                            )
STM_DEMAND.set_distribution(region='UIUC',
                            data=campus_stm_demand,
                            n_seasons=N_seasons,
                            n_hours=N_hours)


# Add technologies
from pygenesys.technology.supply import imp_natgas
from pygenesys.technology.electric import NUCLEAR_ELC, SOLAR_FARM
from pygenesys.technology.storage import LI_BATTERY
from pygenesys.technology.transmission import STM_TUNNEL, TRANSMISSION

# import technology data from EIA
from pygenesys.data.eia_data import get_eia_generators, get_existing_capacity
curr_data = get_eia_generators()


# Set region specific data

import numpy as np
# nuclear cost in M$/MW
years = np.linspace(start_year, end_year, N_years).astype('int')

nuclear_invest = 5.905853
nuclear_fixed = 121.09221
nuclear_variable = 0.009158
nuclear_invest_annual = {}
nuclear_fixed_annual = {}
nuclear_variable_annual = {}

for year in years:
    nuclear_invest_annual[year] = nuclear_invest
    nuclear_fixed_annual[year] = nuclear_fixed
    nuclear_variable_annual[year] = nuclear_variable*(year%2+1)


# add capacity factor data
from pygenesys.data.library import solarfarm_data, railsplitter_data
from pygenesys.utils.tsprocess import four_seasons_hourly

NUCLEAR_ELC.add_regional_data(region='IL',
                              input_comm=ethos,
                              output_comm=electricity,
                              efficiency=1.0,
                              tech_lifetime = 40.0,
                              existing=get_existing_capacity(curr_data,
                                                             'IL',
                                                             'Nuclear'),
                              cost_invest=nuclear_invest,
                              cost_fixed=nuclear_fixed_annual,
                              cost_variable=nuclear_variable_annual,
                              capacity_factor_tech=0.935,
                              ramp_up=0.25,
                              ramp_down=0.25,
                              loan_lifetime=40,
                              emissions={co2eq:1.2e-5}
                              )
solar_cf = four_seasons_hourly(solarfarm_data,
                               kind='CF').flatten()
SOLAR_FARM.add_regional_data(region='IL',
                             input_comm=ethos,
                             output_comm=electricity,
                             efficiency=1.0,
                             tech_lifetime=25,
                             existing=get_existing_capacity(curr_data,
                                                            'IL',
                                                            'Solar Photovoltaic'),
                             capacity_factor_tech=solar_cf,
                             loan_lifetime=15,
                             emissions={co2eq:4.8e-5})

LI_BATTERY.add_regional_data(region='IL',
                             input_comm=electricity,
                             output_comm=electricity,
                             efficiency=0.8,
                             tech_lifetime=15,
                             existing=get_existing_capacity(curr_data,
                                                            'IL',
                                                            'Batteries'),
                             capacity_factor_tech=0.76,
                             storage_duration=8,
                             loan_lifetime=10)

STM_TUNNEL.add_regional_data(region='UIUC',
                             input_comm=[steam, nuclear_steam],
                             output_comm=STM_DEMAND,
                             efficiency=1.00,
                             tech_lifetime=1000,)
TRANSMISSION.add_regional_data(region='IL',
                               input_comm=electricity,
                               output_comm=ELC_DEMAND,
                               efficiency=0.81,
                               tech_lifetime=1000)

co2eq.add_regional_limit(region='IL',
                         limits={2030:100, 2050:0.0})

# Collect the commodities here
demands_list = [ELC_DEMAND, STM_DEMAND]
resources_list = [electricity, steam, ethos, nuclear_steam]
emissions_list = [co2eq]


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    # plt.plot(STM_DEMAND.demand['UIUC'])
    # plt.show()

    print(STM_DEMAND.comm_name)
    STM_DEMAND.comm_name = 'McSteamy'
    print(STM_DEMAND.comm_name)

    print(NUCLEAR_ELC.existing_capacity)
    print(NUCLEAR_ELC.tech_lifetime)

    print(SOLAR_FARM.existing_capacity)
    print(solar_cf)
