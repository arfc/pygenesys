"""
This file contains filepaths to data stored in ``PyGenesys``.

To access the data, simply include the following line in your ``PyGenesys``
input file:

```py
import pygenesys.data.library as pdl
```
or
```py
from pygenesys.data.library import my_data
```
"""

import os
curr_dir = os.path.dirname(__file__)


"""
``campus_elc_demand`` : dataset
columns : [time, kw]
    * ``time`` is a Pandas Datetime index
    * ``kw`` is the average power demand per hour. Units: kW(e)
This dataset represents the hourly demand of electricity usage
at the UIUC campus. However, the _distribution_ of data may be
representative of other campuses or office buildings.
"""
campus_elc_demand = curr_dir + "/uiuc_demand_data.csv"

"""
``campus_stm_demand`` : dataset
columns : [time, kw]
    * ``time`` is a Pandas Datetime index
    * ``kw`` is the average power demand per hour. Units: kW(th)
This dataset represents the hourly demand of steam usage
at the UIUC campus. However, the _distribution_ of data may be
representative of other campuses or office buildings.
"""
campus_stm_demand = curr_dir + "/uiuc_steam_data.csv"
