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

### Clone the Repository

```bash
$ git clone git@github.com:arfc/pygenesys.git
$ cd pygenesys
```

#### Option 1: Basic Installation

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


## Run Tests

The tests can be run by simply executing

```bash
$ pytest
```
