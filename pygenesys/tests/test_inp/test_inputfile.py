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
year_step = 5
N_seasons = 4  # the number of seasons in the model
N_hours = 24  # the number of hours in a day
"""
Note: If the (end_year - start_year) % year_step != 0, then
the final year of the simulation will be truncated.
"""

# Import commodities here
from pygenesys.commodity.demand import ELC_DEMAND

print(ELC_DEMAND.demand)
ELC_DEMAND.add_demand(region='IL', init_demand=183)
ELC_DEMAND.add_demand(region='UIUC', init_demand=4.44)
print(ELC_DEMAND.demand)

print(ELC_DEMAND._db_entry())
print(ELC_DEMAND.comm_label)
# Define System Components
system = {
'IL':{
    'commodities':[ELC_DEMAND],
    'technologies':[]
     },
'UIUC':{
    'commodities':[ELC_DEMAND],
    'technologies':[]
     },
         }
