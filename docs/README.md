# Python for Generating Energy Systems (Pygenesys)

Pygenesys is a modeling tool which generates input files for 
[Temoa](https://github.com/temoaproject/temoa) from python inputs. This folder 
contains the documentation for Pygenesys generated with Sphinx. To learn more about
using Sphinx, check out their 
[Using Sphinx](https://www.sphinx-doc.org/en/master/usage/index.html) guides. For 
the purposes of the existing documentation, all you have to do to generate the docs
is run: 
```
make html
```
from this folder. The documentation will be generated in html format under 
`_build/html`, and you can use a web browser to interact with them as a website.

## Contributing to the Docs

First, consult the CONTRIBUTING document (*in progress*). We recommend being
passingly familiar with 
[reStructuredText](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html)
, though it is not a pre-requiste. Then you should be equipped to address issues from 
the [GitHub repo](https://github.com/arfc/pygenesys/issues), or add additional 
documentation to help users and developers alike! Most of the documenation is 
auto-generated from python docstrings in the 
[numpy style](https://numpydoc.readthedocs.io/en/latest/format.html).