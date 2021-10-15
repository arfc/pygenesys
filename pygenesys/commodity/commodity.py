from pygenesys.utils.growth_model import choose_growth_method
from pygenesys.utils.tsprocess import choose_distribution_method
import numpy as np

# ==============================================================================
# ==============================================================================
# Defines Commodity
# ==============================================================================
# ==============================================================================


class Commodity(object):
    """
    A ''commodity'' is a "raw material" or an "energy carrier."
    This class contains information about a commodity used in a
    Temoa model.
    """

    def __init__(self,
                 comm_name,
                 units,
                 comm_label='p',
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
        return (f"(\"{self.comm_name}\"," +
                f"\"{self.comm_label}\"," +
                f"\"{self.description} in {self.units}\")")

    def _db_entry(self):
        return (self.comm_name,
                self.comm_label,
                self.description + ", " + self.units)

# ==============================================================================
# ==============================================================================
# Defines DemandCommodity
# ==============================================================================
# ==============================================================================


class DemandCommodity(Commodity):
    """
    This class holds data for a demand commodity in Temoa.
    """

    def __init__(self,
                 comm_name,
                 units,
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
        demand : dictionary
            The dictionary containing the commodity demand for a given
            region.
        """
        super().__init__(comm_name,
                         units,
                         comm_label,
                         description,)
        self.demand = {}
        self.distribution = {}

        return

    def add_demand(self,
                   region,
                   init_demand,
                   start_year,
                   end_year,
                   N_years,
                   growth_rate=0.0,
                   growth_method='linear',
                   ):
        """
        Updates the ``demand`` dictionary with a new region and demand.

        Parameters
        ----------
        region : string
            The label for a region.
        init_demand : float
            The demand for a commodity in the first year of the simulation.
        start_year : integer
            The first year of the simulation.
        end_year : integer
            The last year of the simulation.
        N_years : integer
            The number of years simulated between ``start_year`` and
            ``end_year``.
        growth_rate : float
            The rate of growth for the given quantity. Default is zero growth.
        growth_method : string
            Specifies how the future demand will grow. Default is linear.
        """

        growth_calculator = choose_growth_method(growth_method)
        demand_forecast = growth_calculator(init_demand,
                                            start_year,
                                            end_year,
                                            N_years,
                                            growth_rate)

        if region in self.demand:
            print(f'Region {region} already in database. Overwriting.')
            self.demand[region] = demand_forecast
        else:
            self.demand.update({region: demand_forecast})

        return

    def set_distribution(self,
                         region,
                         data,
                         n_seasons=4,
                         n_hours=24,
                         normalize=True,
                         kind='demand'):
        """
        This function generates a distribution time series. The sum
        of this distribution must be equal to unity. If users
        do not specify a distribution, the demand will be uniform in
        each time slice. If data is supplied, it should have at least
        the same temporal resolution as the number of hours and number
        of seasons.
        E.g.
        Suppose:
            N_seasons = 4
            N_hours = 24

        Then:
            The data should have at least a year's worth of hourly data.

        Parameters
        ----------
        region : string
            The region identifier.
        data_path : string
            The path to the data.
        """
        if normalize:
            distribution_calculator = choose_distribution_method(n_seasons,
                                                                 n_hours)
            distribution = distribution_calculator(data,
                                                   n_seasons,
                                                   n_hours,
                                                   kind)
        elif not normalize:
            distribution = data


        self.distribution[region] = distribution.flatten()

        return
# ==============================================================================
# ==============================================================================
# Defines EmissionsCommodity
# ==============================================================================
# ==============================================================================


class EmissionsCommodity(Commodity):
    """
    This class holds data for an emissions commodity in Temoa.
    """

    def __init__(self,
                 comm_name,
                 units,
                 limit=None,
                 years=None,
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
                         units,
                         comm_label,
                         description,)

        self.emissions_limit = {}

        return

    def add_regional_limit(self,
                           region,
                           limits,):
        """
        This function adds an emissions limit for a particular year
        or set of years.

        Parameters
        ----------
        region : string
            The region of interest. This region must have technologies
            that produce this emission.
        limits : dictionary
            A dictionary with years for keys and the emissions limits
            for values. **Every year must be a simulation year.**

            **Under consideration: applying a limit to the nearest
            year in the simulation to the one provided.**
            E.g. years in simulation = [2021, 2026, 2031];
                 constraint year = 2025
                 The constraint would be applied to 2026, rather than
                 requiring the constraint year be exactly 2026 or
                 similar.
        """

        if region in self.emissions_limit:
            print(f'Region {region} already in database. Overwriting.')
            self.emissions_limit[region] = limits
        else:
            self.emissions_limit.update({region: limits})

        return


if __name__ == "__main__":

    bacon = Commodity(comm_name='bacon',
                      comm_label='food',
                      units='strips')

    print(bacon.comm_name)
    print(repr(bacon))
    print(bacon._db_entry())

    pancakes = DemandCommodity(comm_name='pancakes',
                               units='number',
                               )
    print(repr(pancakes))
    print(pancakes._db_entry())

    ELC_DEMAND = DemandCommodity(comm_name='ELC_DEMAND',
                                 units='GWh',
                                 description='End-use electricity demand')

    print(repr(ELC_DEMAND))
    print(ELC_DEMAND._db_entry())
    print(ELC_DEMAND.units)
