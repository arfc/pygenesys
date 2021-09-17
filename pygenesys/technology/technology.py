
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
                 units,
                 capacity_to_activity,
                 tech_sector='energy',
                 tech_label='p',
                 description='',
                 category='',
                 reserve_tech=False,
                 ramping_tech=False,
                 storage_tech=False
                 ):
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
        capacity_to_activity : float
            This specifies how much of commodity, A, can be produced by
            capacity, C, in one year. E.g. 1 MWe can produce 8760 MWh(e)
            in one year.
        tech_lifetime : integer
            The operational lifetime of the technology.
        loan_lifetime : integer
            The ammortization period of the technology invest cost.
        description : string
             A short 1-4 word description of the technology.
        category : string
            The fuel category of the technology. Optional attribute.
        reserve_tech : boolean
            Indicates if the technology will be held in reserve to meet
            the planning reserve margin.
        ramping_tech : boolean
            Indicates if the technology has a ramp rate. Only valid for
            non-intermittent technologies.
        """
        self._type = 'Technology'
        self.tech_name = tech_name
        self.tech_sector = tech_sector
        self.tech_label = tech_label
        self.description = description
        self.units = units
        self.capacity_to_activity = capacity_to_activity
        self.category = category
        self.reserve_tech = reserve_tech
        self.ramping_tech = ramping_tech
        self.storage_tech = storage_tech
        self.regions = []
        self.input_comm = {}
        self.output_comm = {}
        self.efficiency = {}
        self.existing_capacity = {}
        self.tech_lifetime = {}
        self.loan_lifetime = {}
        self.cost_variable = {}
        self.cost_fixed = {}
        self.cost_invest = {}
        self.capacity_factor_tech = {}
        self.ramp_up = {}
        self.ramp_down = {}
        self.storage_duration = {}
        self.emissions = {}

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

    def add_regional_data(self,
                          region,
                          **kwargs):
        """
        This function adds regional data for each parameter.
        Non-required items are kwargs.


        """
        attr_dict = {
            "input_comm": self.input_comm,
            "output_comm": self.output_comm,
            "regions": self.regions,
            "tech_lifetime": self.tech_lifetime,
            "loan_lifetime": self.loan_lifetime,
            "cost_variable": self.cost_variable,
            "cost_fixed": self.cost_fixed,
            "cost_invest": self.cost_invest,
            "efficiency": self.efficiency,
            "existing": self.existing_capacity,
            "capacity_factor_tech": self.capacity_factor_tech,
            "ramp_up": self.ramp_up,
            "ramp_down": self.ramp_down,
            "storage_duration": self.storage_duration,
            "emissions": self.emissions
        }

        # check if region is a list or a string
        if isinstance(region, str):
            if region in self.regions:
                pass
            else:
                self.regions.append(region)
            for kw in kwargs:
                print(kw, kwargs[kw])
                attribute = attr_dict[kw]
                attribute[region] = kwargs[kw]

        elif isinstance(region, list):
            self.regions += region
            self.regions = list(np.unique(self.regions))
            for kw in kwargs:
                print(kw, kwargs[kw])
                attribute = attr_dict[kw]
                for pl in region:
                    attribute[pl] = kwargs[kw]

        print(self.input_comm)
        print(self.output_comm)
        print(self.efficiency)
        return


if __name__ == '__main__':
    pass
