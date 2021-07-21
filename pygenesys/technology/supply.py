"""
This file contains information for pre-made import technologies. These
technologies serve to "create" basic energy carriers, like natural gas or
gasoline.
"""

from pygenesys.technology.technology import Technology
from pygenesys.commodity.resource import ethos, natural_gas

imp_natgas = Technology(tech_name='IMP_NATGAS',
                        input_comm=ethos,
                        output_comm=natural_gas,
                        units="MMBTU/hr",
                        tech_sector='supply',
                        tech_lifetime=1000,
                        loan_lifetime=None,
                        )


if __name__ == '__main__':
    print(isinstance(imp_natgas, Technology))
    print(imp_natgas._type)
