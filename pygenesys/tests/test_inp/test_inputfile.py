"""
PyGenesys Input File
To run execute:

```bash
genesys --infile my/pygenesys/input/file.py
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
year_step = 5
N_seasons = 4  # the number of seasons in the model
N_hours = 24  # the number of hours in a day
"""
Note: If the (end_year - start_year) % year_step != 0, then
the final year of the simulation will be truncated.
"""
# Commodities Section
demand = None
physical = None
byproducts = None
