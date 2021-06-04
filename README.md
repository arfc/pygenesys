# Python for Generating Energy Systems (PyGenESys)

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

``PyGenesys`` is a package that is intended to be a simple and intuitive interface to run Temoa.

#### Step 1: Create your input file.
A ``PyGenesys`` input file is written in Python with clear and verbose variable names. The
beginning should look something like this:

```py
import os
curr_dir = os.path.dirname(__file__)

database_filename = 'my_temoadb.sqlite'  # where the database will be written
scenario_name = 'test'
start_year = 2025
end_year = 2050
year_step = 5
N_seasons = 4 # the number of seasons in the model
N_hours = 24 # the number of hours in a day
```

The first two lines

```py
import os
curr_dir = os.path.dirname(__file__)
```
are recommended, but not required. These lines tell ``PyGenesys`` to save the
database in the same directory as your input file. Otherwise, the database will
be saved in the ``pygenesys/pygenesys`` folder.

**TODO: Add Detail**

#### Step 2: Build the database
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


### Credits and Acknowledgments

Some of the code in ``driver.py`` was borrowed and modified from another open
source project [``PyRK``](https://github.com/pyrk/pyrk).
