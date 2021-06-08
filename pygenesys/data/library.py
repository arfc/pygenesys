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
This dataset represents the hourly demand of electricity usage
at the UIUC campus. However, the _distribution_ of data may be
representative of other campuses or office buildings.
"""
campus_elc_demand = curr_dir+"/uiuc_demand_data.csv"
