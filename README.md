# Python for Generating Energy Systems (PyGenesys)

This package can be used to generate input files for the [Temoa](https://github.com/temoaproject/temoa) modelling tool. Transparency and repeatability are integral to the design motivations for Temoa. PyGenesys takes this concept
even further by reducing the lead time and programming background required to
run Temoa.
PyGenesys offers technology models with cost and production time series data.
The basic model is based on the state of Illinois and its flagship university, the University of Illinois at Urbana-Champaign.

## Install Temoa (TODO: add details)

Clone the repository and create a conda environment

```bash
git clone git@github.com:temoaproject/temoa.git
cd temoa
conda env create
conda activate temoa-py3
```


## Install PyGenesys

The installation is quite simple:

### Step 1: Clone the Repository

```bash
$ git clone git@github.com:arfc/pygenesys.git
$ cd pygenesys
```
### Step 2:

There are two options for installation after cloning the repository. If you
don't plan on editing the source code, use the first option.

#### Option 1: Basic Installation (default)

```bash
$ pip install .
```

#### Option 2: Editable Installation
This option is for people that want to develop PyGenesys. By doing
this method, any changes you make to the PyGenesys source code will
take immediate effect on your local machine.

```bash
$ pip install -e .
```

and you're done!

## Running PyGenesys

``pygenesys`` is a package that is intended to be a simple and intuitive interface to run Temoa.

### Step 1: Create your input file.

#### Step 1.1: Simulation Metadata
A ``pygenesys`` input file is written in Python with clear and verbose variable names. The
beginning should look something like this:

```py
import os
curr_dir = os.path.dirname(__file__)

folder = 'data_files'
database_filename = f'{folder}/my_temoadb.sqlite'  # where the database will be written
scenario_name = 'test'
start_year = 2025
end_year = 2050
N_years = 5
N_seasons = 4 # the number of seasons in the model
N_hours = 24 # the number of hours in a day
```

The first two lines

```py
import os
curr_dir = os.path.dirname(__file__)
```
are recommended, but not required. These lines tell ``pygenesys`` to save the
database in the same directory as your input file. Otherwise, the database will
be saved in the ``pygenesys/pygenesys`` folder.

#### Step 1.2: Optional Parameters

The parameters
* ``reserve_margin`` (The fraction of excess capacity, for grid reliability)
* ``discount_rate`` (The global discount rate)

are optional global parameters.

```py
reserve_margin = {'region':0.15}
discount_rate = 0.05  
```

#### Step 1.3: Initialize Demand Commodities

Users should design their energy systems from right to left. Begin by
initializing the end-use demands. You can use either a preset commodity
located in ``pygenesys.commodity.demand`` or build your own using the
``DemandCommodity`` class.

```py
# Method 1:
from pygenesys.commodity.demand import ELC_DEMAND  # initialized

# Method 2:
from pygenesys.commodity.commodity import DemandCommodity

H2 = DemandCommodity(comm_name='H2',
                     units='kg',
                     description='hydrogen')

# initialized
```

#### Step 1.4 Set Demand Growth and Distribution

This step answers the following questions:
1. How much of each commodity should Temoa produce?
2. When should the commodity be produced (e.g. mostly at night, peak hours, etc.)?
3. How does the demand change over time?
4. How does the demand vary by region?

Users should call ``DemandCommodity.add_demand()`` and ``DemandCommodity.set_distribution``.

```py
ELC_DEMAND.add_demand(region='region',  # specifies the region
                      init_demand=445.87,  # the demand in first simulation year
                      start_year=start_year,  # starting year
                      end_year=end_year,  # ending year
                      N_years=N_years,  # number of years
                      growth_rate=0.01,  # modeled growth rate
                      growth_method='linear')  # how does the growth change?

H2.add_demand(region='region',
              init_demand=100,
              start_year=start_year,
              end_year=end_year,
              N_years=N_years,
              growth_rate=0.00)  # growth rate of zero means demand is constant
```

Users should call ``DemandCommodity.add_demand`` for each unique region and
demand commodity.
**In the future, this function will accept a list for ``region`` if all regions
have the same forecast.**

The Demand distribution specifies load profiles. For example, electricity demand
might peak in the summer at noon and natural gas demand might peak in the
winter at night. This method specifies those differences.

** PyGenesys currently only handles demand distributions with 24 hour slices and
four annual seasons. Distributions for time slices with fewer or more time slices
should be generated manually and passed as a list or numpy array.**

PyGenesys has a small library of built in data in ``pygenesys.data.library``.

```py
from pygenesys.data.library import campus_elc_demand

ELC_DEMAND.set_distribution(region='region',
                            data=campus_elc_demand,
                            n_seasons=N_seasons,
                            n_hours=N_hours)

# passing no distribution for H2 will default to a uniform distribution.
```

#### Step 1.5 Add technologies to meet ultimate demands

``DemandCommodity`` objects represent ultimate demands. They must be generated
somehow. They can be created directly from a production technology (e.g. a
power plant) or they can be "transported" using a transmission technology. The
latter is beneficial if the final demand and intermediate energy carriers are
similar. For example if you want to use electricity for electric cars and also
have an aggregated electricity demand.

```py
from pygenesys.commodity.resource import electricity  # an intermediate resource
from pygenesys.technology.transmission import TRANSMISSION

from pygenesys.commodity.commodity import Commodity

hydrogen = Commodity(comm_name='hydrogen',
                     units='kg',
                     description='hydrogen')
```

Users must also specify unique regional data for each technology by calling
``Technology.add_regional_data()``.

```py
TRANSMISSION.add_regional_data(region='region',
                               input_comm=electricity,
                               output_comm=ELC_DEMAND,
                               efficiency=1.0,
                               tech_lifetime=1000,)
```

Similar to ``DemandCommodity``, users can create their own technologies
using the ``Technology`` class.

```py
from pygenesys.technology.technology import Technology
H2_PIPES = Technology(tech_name='H2_PIPES',
                      units='kg-hours',
                      tech_sector='hydrogen',
                      tech_label='p',
                      description='hydrogen transport',
                      category='transmission',
                      capacity_to_activity=1.00,)  # C2A is required

H2_PIPES.add_regional_data(region='region',
                           input_comm=hydrogen,
                           output_comm=H2,
                           efficiency=1.0,
                           tech_lifetime=1000,)                      
```

The technology lifetimes for "dummy" technologies are usually much longer
than the simulation time because it can be built once to emphasize the importance
of other technology choices. These are, of course, tunable parameters if one
wishes to model transmission costs.

#### Step 1.6 Add technologies to produce energy carriers

So far we only have dummy technologies that can supply ultimate demands and
will pull from dummy commodities. Let's make those commodities real. The only
difference is that these technologies must have the desired energy carrier
as their output commodity.

If the region you're modeling is at the state or county level in the United States,
then you can access EIA data about those technologies using ``pygenesys.data.eia_data``.

```py
from pygenesys.data.eia_data import get_eia_generators, get_existing_capacity
curr_data = get_eia_generators()

from pygenesys.technology.electric import NUCLEAR_ELC
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


# Add more! As an exercise, try creating an electrolyzer to make hydrogen...
```

#### Step 1.7 Finalizing the input file

As a final step, users should collect all of the commodities they use by _type_.

```py
# copy and paste these lines, then fill in...
demands_list = []
resources_list = []
emissions_list = []
```

This will be deprecated, eventually, and replaced with a function that automatically
collects the commodities by reading the input file.

If you want to check your input file, plot any data, or make some scratch
calculations, you can use
```py
if __name__ == "__main__":

  # your scratch work here!

  import matplotlib.pyplot as plt
  plt.style.use('ggplot')

  plt.plot(ELC_DEMAND.demand['region'][0])
  plt.show()
```

In fact, this feature is one of the advantages of using a python script as an
input file!

### Step 2: Build the database
Now that you have an input file, you can build the SQLite database required
by Temoa via:

```bash
$ genesys --infile path/to/my/input/file.py
```
**Note: This command can be run from any directory.**

## Run Tests

The tests can be run by executing the following command from the top level
directory of ``pygenesys``.

```bash
$ pytest
```

## Rendering the docs

The documentation is generated using sphinx with numpy style docstrings,
to render them locally run:

```bash
$ cd docs
$ make html
```

## Contributing to the Docs

First, consult the CONTRIBUTING document (*in progress*). We recommend being
passingly familiar with 
[reStructuredText](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html)
, though it is not a pre-requiste. Then you should be equipped to address issues from 
the [GitHub repo](https://github.com/arfc/pygenesys/issues), or add additional 
documentation to help users and developers alike! Most of the documenation is 
auto-generated from python docstrings in the 
[numpy style](https://numpydoc.readthedocs.io/en/latest/format.html).

### Credits and Acknowledgments

Some of the code in ``driver.py`` was borrowed and modified from another open
source project [``PyRK``](https://github.com/pyrk/pyrk).
