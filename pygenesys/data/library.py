"""
This file contains filepaths to data stored in ``PyGenesys``.

To access the data, simply include the following line in your ``PyGenesys``
input file:

```py
import pygenesys.data.library as pdl

x = pdl.my_data
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

"""
``railsplitter_data`` : dataset
columns : [time, kw]
    * ``time`` is a Pandas Datetime index
    * ``MWh`` is the average power produced per hour. Units: MWh
This dataset represents the hourly wind power generation at Railsplitter
Wind Farm from 2016 to 2019 that was sent to the University of Illinois.
"""
railsplitter_data = curr_dir + "/railsplitter_data.csv"

"""
``railsplitter_data`` : dataset
columns : [time, kw]
    * ``time`` is a Pandas Datetime index
    * ``MWh`` is the average power produced per hour. Units: MWh
This dataset represents the hourly wind power generation at Railsplitter
Wind Farm from 2016 to 2019 that was sent to the University of Illinois.
"""
solarfarm_data = curr_dir + "/solarfarm_data.csv"

"""
``eia_electric_generators`` : dataset
From the EIA website: https://www.eia.gov/electricity/data/eia860m/
Contains data for all of the operating generators in the United States.
"""

eia_electric_generators = curr_dir + "/april_generator2021.xlsx"

"""
``nrel_electric_costs`` : dataset
From the National Renewable Energy Laboratory Annual Technology Baseline.
NREL also offers a transportation dataset in the 2021 ATB.
"""
nrel_electric_costs = curr_dir + "/ATBe.csv"


if __name__ == "__main__":
    import pandas as pd
    import numpy as np


    df = pd.read_csv(nrel_electric_costs, usecols=['atb_year',
                                                   'core_metric_parameter',
                                                   'technology',
                                                   'techdetail',
                                                   'scenario',
                                                   'core_metric_variable',
                                                   'value',
                                                   'units'])
    df = df[df['core_metric_parameter']=='Fuel']
    print(df.head())
