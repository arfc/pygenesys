"""
A ''commodity'' is a "raw material" or an "energy carrier."
"""

class Commodity(object):
    """
    A ''commodity'' is a "raw material" or an "energy carrier.
    This class contains information about a commodity used in a
    Temoa model.
    """

    def __init__(self,
                 comm_name,
                 comm_label,
                 units,
                 description='',
                 ):
        """
        This class contains information about a commodity used
        in a Temoa model.

        Parameters
        ----------
        comm_name : string
            The name of the commodity.
        comm_label : string
            The commodity label indicates the commodity type.
            Currently accepted values: 'p', 'd', 'e'
        units : string
            The units of the commodity. E.g. Electricity might
            be in units of megawatt-hours. Hydrogen might be in
            units of kilograms.
            TODO: Add support for ``pint`` in order to automate unit
            checking.
        description : string
            A brief (1-4 words) description of the commodity.
        """
        self.comm_name = comm_name
        self.comm_label = comm_label
        self.units = units
        self.description = description

        return


    def __repr__(self):
        return (f"(\"{self.comm_name}\","+
                f"\"{self.comm_label}\","+
                f"\"{self.description} in {self.units}\")")


    def _db_entry(self):
        return (self.comm_name,
                self.comm_label,
                self.description + self.units)

class DemandCommodity(Commodity):
    """
    This class holds data for a demand commodity in Temoa
    """

    def __init__(self,
                 comm_name,
                 units,
                 demand,
                 growth_rate = 0.0,
                 growth_method = 'linear',
                 demand_distribution=None,
                 comm_label='d',
                 description='',
                 ):
        """
        This class contains data for a demand commodity used
        in a Temoa model.

        Parameters
        ----------
        comm_name : string
            The name of the commodity.
        comm_label : string
            The commodity label indicates the commodity type.
            Default: 'd'
        units : string
            The units of the commodity. E.g. Electricity might
            be in units of megawatt-hours. Hydrogen might be in
            units of kilograms.
            TODO: Add support for ``pint`` in order to automate unit
            checking.
        description : string
            A brief (1-4 words) description of the commodity.
        demand : float, list
            The quantity of the commodity that is demanded for a given year
            in the simulation.
        """
        super().__init__(comm_name,
                         comm_label,
                         units,
                         description,)
        self.demand = demand
        self.demand_distribution = demand_distribution

        return


class EmissionsCommodity(Commodity):
    """
    This class holds data for a demand commodity in Temoa
    """

    def __init__(self,
                 comm_name,
                 units,
                 limit = None,
                 years = None,
                 comm_label='e',
                 description='',
                 ):
        """
        This class contains data for an emissions commodity used
        in a Temoa model.

        Parameters
        ----------
        comm_name : string
            The name of the commodity.
        comm_label : string
            The commodity label indicates the commodity type.
            Default: 'e'
        units : string
            The units of the commodity. E.g. Electricity might
            be in units of megawatt-hours. Hydrogen might be in
            units of kilograms.
            TODO: Add support for ``pint`` in order to automate unit
            checking.
        description : string
            A brief (1-4 words) description of the commodity.
        """
        super().__init__(comm_name,
                         comm_label,
                         units,
                         description,)
        self.demand = demand
        self.demand_distribution = demand_distribution

        return



if __name__ == "__main__":

    bacon = Commodity(comm_name = 'bacon',
                      comm_label='food',
                      units = 'strips')


    print(bacon.comm_name)
    print(repr(bacon))
    print(bacon._db_entry())

    pancakes = DemandCommodity(comm_name = 'pancakes',
                               units = 'number',
                               demand = 125)
    print(repr(pancakes))
    print(pancakes._db_entry())
