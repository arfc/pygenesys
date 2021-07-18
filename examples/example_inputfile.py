"""
PyGenesys Input File
To run execute:

```bash
genesys --infile test_inputfile.py
```
"""
# So the database can be saved in the location from which
# the command is called.
from pygenesys.technology.supply import imp_natgas
from pygenesys.commodity.resource import electricity, steam, ethos
from pygenesys.data.library import campus_elc_demand, campus_stm_demand
from pygenesys.commodity.demand import ELC_DEMAND, STM_DEMAND
import os
curr_dir = os.path.dirname(__file__)

database_filename = 'my_temoadb.sqlite'  # where the database will be written
scenario_name = 'test'
start_year = 2025
end_year = 2050
N_years = 6
N_seasons = 4  # the number of seasons in the model
N_hours = 24  # the number of hours in a day

# Import commodities here
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


# Collect the commodities here
demands_list = [ELC_DEMAND, STM_DEMAND]
resources_list = [electricity, steam, ethos]
emissions_list = []


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    # plt.plot(STM_DEMAND.demand['UIUC'])
    # plt.show()

    print(STM_DEMAND.comm_name)
    STM_DEMAND.comm_name = 'McSteamy'
    print(STM_DEMAND.comm_name)
