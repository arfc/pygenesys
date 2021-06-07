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
regions = ['IL']  # specify the regions in the simulation
start_year = 2025
end_year = 2050
N_years = 6
N_seasons = 4  # the number of seasons in the model
N_hours = 24  # the number of hours in a day

# Import commodities here
from pygenesys.commodity.demand import ELC_DEMAND, STM_DEMAND
ELC_DEMAND.add_demand(region='IL', init_demand=183)
ELC_DEMAND.add_demand(region='UIUC', init_demand=4.44)
ELC_DEMAND.add_demand(region='UIUC', init_demand=33)
print(ELC_DEMAND.demand)

print('steam')
print(STM_DEMAND.demand)
STM_DEMAND.add_demand(region='UIUC', init_demand=6)

print(STM_DEMAND.demand)
print(ELC_DEMAND._db_entry())
print(STM_DEMAND._db_entry())


from pygenesys.commodity.resource import electricity, steam

# Collect the commodities here
demands_list = [ELC_DEMAND, STM_DEMAND]
resources_list = [electricity, steam]
emissions_list = []
