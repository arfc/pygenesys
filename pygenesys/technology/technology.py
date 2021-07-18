
# ==============================================================================
# ==============================================================================
# Defines Technology
# ==============================================================================
# ==============================================================================


class Technology(object):
    """
    This class holds the information for technologies
    in a Temoa simulation. A ``Technology`` transforms
    one energy carrier into another. E.g. a nuclear plant
    might transform a uranium commodity into heat or electricity.
    """

    def __init__(self,
                 tech_name,
                 input_comm,
                 output_comm,
                 units,
                 regions=[],
                 tech_lifetime=None,
                 loan_lifetime=None,
                 cost_variable=None,
                 cost_fixed=None,
                 cost_capital=None,
                 tech_sector='energy',
                 tech_label='p',
                 description='',
                 category=''):
        """
        This class contains information about a technology used
        in a Temoa model.

        Parameters
        ----------
        tech_name : string
            The name of the technology
        tech_label : string
            The label of the technology. Describes how the technology
            is used in Temoa. Currently accepts:
            * 'r' (resource import)
            * 'p' (production, general)
            * 'ps' (production, storage)
            * 'pb' (production, baseload)
        tech_sector : string
            The name of the technology sector. E.g. residential, electric,
            industrial. This option is used to group technologies by sector
            in post-processing steps.
        input_comm : Commodity object
            The commodity that a technology receives as input and
            subsequently transforms.
        output_comm : Commodity object
            The commodity that a technology outputs after transforming
            the input commodity.
        units : string or pint Quantity object.
            This specifies the units for the technology. Helps
            calculate the ``cap2act`` property for the ``Capacity2Activity
            table in Temoa.
        tech_lifetime : integer
            The operational lifetime of the technology.
        loan_lifetime : integer
            The ammortization period of the technology capital cost.
        description : string
             A short 1-4 word description of the technology.
        category : string
            The fuel category of the technology. Optional attribute.
        """
        self._type = 'Technology'
        self.tech_name = tech_name
        self.tech_sector = tech_sector
        self.tech_label = tech_label
        self.description = description
        self.category = category
        self.input_comm = input_comm
        self.output_comm = output_comm
        self.units = units
        self.regions = regions
        self.tech_lifetime = tech_lifetime
        self.loan_lifetime = loan_lifetime
        self.cost_variable = cost_variable
        self.cost_fixed = cost_fixed
        self.cost_capital = cost_capital

        return

    def __repr__(self):
        return (f"{self._type}" +
                f"(\"{self.tech_name}\"," +
                f"\"{self.tech_label}\"," +
                f"\"{self.units}\")")

    def _db_entry(self):
        return (self.tech_name,
                self.tech_label,
                self.tech_sector,
                self.description + ", " + self.units,
                self.category)

    def add_tech_data(self,
                      region,
                      **kwargs):
        """
        This function adds regional data for each parameter.
        Non-required items are kwargs.


        """
        # check if region is a list or a string.

        # check if region already exists
        if region in self.regions:
            print(f'Technology already exists in the {region} region.' +
                  'Overwriting.')
        else:
            self.regions.append(region)

        return


if __name__ == '__main__':
    t = Technology(tech_name='kitchenaid',
                   input_comm='flour',
                   output_comm='dough',
                   units='lbs',
                   tech_sector='home')

    print(t._db_entry())
    print(repr(t))

    if isinstance(t, Technology):
        print('success')
    else:
        print('fail')

    print(t._type)
