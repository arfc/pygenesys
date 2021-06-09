"""
PyGenesys Input File
To run execute:

```bash
genesys --infile test_inputfile.py
```
"""
# So the database can be saved in the location from which
# the command is called.
import os
curr_dir = os.path.dirname(__file__)

database_filename = 'my_temoadb.sqlite'  # where the database will be written
scenario_name = 'test'
start_year = 2025
end_year = 2050
N_years = 6
N_seasons = 365  # the number of seasons in the model
N_hours = 24  # the number of hours in a day

# Import commodities here
from pygenesys.commodity.demand import ELC_DEMAND, STM_DEMAND
ELC_DEMAND.add_demand(region='IL',
                      init_demand=183,
                      start_year=start_year,
                      end_year = end_year,
                      N_years = N_years,
                      growth_rate=0.01)
ELC_DEMAND.add_demand(region='UIUC',
                      init_demand=4.44,
                      start_year=start_year,
                      end_year = end_year,
                      N_years = N_years,
                      growth_rate=0.01)
STM_DEMAND.add_demand(region='UIUC',
                      init_demand=6,
                      start_year = start_year,
                      end_year = end_year,
                      N_years = N_years,
                      growth_rate=0.01,
                      growth_method='exponential')

# Import distribution data
from pygenesys.data.library import campus_elc_demand, campus_stm_demand
ELC_DEMAND.set_distribution(region='UIUC',
                            data_path=campus_elc_demand,
                            n_seasons=N_seasons,
                            n_hours=N_hours
                            )
STM_DEMAND.set_distribution(region='UIUC',
                            data_path=campus_stm_demand,
                            n_seasons=N_seasons,
                            n_hours=N_hours)

from pygenesys.commodity.resource import electricity, steam

# Collect the commodities here
demands_list = [ELC_DEMAND, STM_DEMAND]
resources_list = [electricity, steam]
emissions_list = []
