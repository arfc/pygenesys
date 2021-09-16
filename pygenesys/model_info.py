import numpy as np
import sqlite3
from pygenesys.utils.db_creator import *


class ModelInfo(object):
    """
    This class holds information about the PyGenesys and
    Temoa model.
    """

    def __init__(self,
                 output_db,
                 scenario_name,
                 start_year,
                 end_year,
                 N_years,
                 N_seasons,
                 N_hours,
                 technologies,
                 demands,
                 resources,
                 emissions,
                 reserve_margin):
        """
        This class holds information about the PyGenesys and
        Temoa model.

        Parameters
        ----------
        output_db : string
            The name and path of the output database.
        scenario_name : string
            The name of the scenario this model will run.
        start_year : int
            The first year of the model simulation
        end_year : int
            The last year of the model simulation
        year_step : int
            The time between simulated years. E.g. if the
            year_step is 5 and the first year is 2020, then
            the next year in the simulation will be 2025.
        N_seasons : int
            The number of seasons in the simulation. Several values
            are acceptable. E.g.
                * 1; there are no seasonal differences (not implemented)
                * 4; spring,summer,fall,winter
                * 365; full year, daily resolution
        N_hours : int
            The number of hours in the simulation. Several values
            are acceptable. E.g.
                * 1; there is no daily variation  (not implemented)
                * 2; diurnal variation, step function (not implemented)
                * 24; full day, hourly resolution
        commodities : dictionary
            A dictionary of the demand, resource, and emissions commodities.
        technologies : list
            A list of ``Technology`` objects
        reserve_margin : float
            The value of the "planning reserve margin." This value forces
            Temoa to include enough excess capacity above peak demand to
            ensure reliability. E.g. reserve_margin = 0.3 corresponds to
            a Planning Reserve Margin of 30 percent, or total generating
            capacity that is 30 percent greater than the annual peak demand.
        """

        self.output_db = output_db
        self.scenario_name = scenario_name
        self.start_year = start_year
        self.end_year = end_year
        self.N_years = N_years
        self.N_seasons = N_seasons
        self.N_hours = N_hours
        self.commodities = {
            'demand': demands,
            'resources': resources,
            'emissions': emissions
        }
        self.technologies = technologies
        self.reserve_margin = reserve_margin

        # derived quantities
        self.time_horizon = self._calculate_time_horizon()
        self.existing_years = self._collect_existing_years()
        self.seg_frac = self._calculate_seg_frac()
        self.regions = self._collect_regions()
        self.tech_sectors = self._collect_tech_sectors()


        return

    def _calculate_time_horizon(self):
        """
        Calculates the complete simulation time horizon.
        Defines the "future" time periods in the Temoa
        database.
        """

        years = np.linspace(self.start_year,
                            self.end_year,
                            self.N_years).astype('int')

        return years

    def _calculate_seg_frac(self):
        """
        Calculates the fraction of a year represented
        by each time slice.
        Defines the values for the "SegFrac" table
        in the Temoa database.
        """

        seg_frac = 1 / (self.N_seasons * self.N_hours)

        return seg_frac

    def _collect_regions(self):

        regions = []
        for demand_comm in self.commodities['demand']:
            comm_regions = list(demand_comm.demand.keys())
            for r in comm_regions:
                regions.append(r)

        return np.unique(regions)

    def _collect_tech_sectors(self):

        sectors = np.unique([t.tech_sector for t in self.technologies])

        return sectors


    def _collect_existing_years(self):
        """
        Collects a unique list of existing years from the technologies
        in the model.
        """
        years = []
        for tech in self.technologies:
            for place in tech.regions:
                ex_years = list(tech.existing_capacity[place].keys())
                years += ex_years

        return np.unique(years)


    def _write_sqlite_database(self):
        """
        Writes model info directly to an sqlite database.
        """

        conn = establish_connection(self.output_db)

        # create fundamental tables
        seasons = create_time_season(conn, self.N_seasons)
        create_time_period_labels(conn)
        create_time_periods(conn, self.time_horizon, self.existing_years)
        # create_existing_periods(conn, self.technology_list)
        time_slices = create_time_of_day(conn, self.N_hours)
        create_segfrac(conn, self.seg_frac, seasons, time_slices)
        create_regions(conn, self.regions)
        create_commodity_labels(conn)
        create_commodities(conn, self.commodities)
        create_demand_table(conn,
                            self.commodities['demand'],
                            self.time_horizon)
        create_demand_specific_distribution(conn,
                                            self.commodities['demand'],
                                            time_slices,
                                            seasons)
        create_technology_labels(conn)
        create_sectors(conn, self.tech_sectors)
        create_technologies(conn, self.technologies)
        create_existing_capacity(conn, self.technologies, self.time_horizon)
        create_efficiency(conn, self.technologies, self.time_horizon)
        create_lifetime_tech(conn, self.technologies)
        create_invest_cost(conn, self.technologies, self.time_horizon)
        create_variable_cost(conn, self.technologies, self.time_horizon)
        create_fixed_cost(conn, self.technologies, self.time_horizon)
        create_capacity_factor_tech(conn,
                                    self.technologies,
                                    time_slices,
                                    seasons)
        create_reserve_margin(conn, self.reserve_margin)
        create_tech_reserve(conn, self.technologies)

        # output tables
        create_output_vcapacity(conn)
        create_output_vflow_out(conn)
        create_output_vflow_in(conn)
        create_output_objective(conn)
        create_output_curtailment(conn)
        create_output_emissions(conn)
        create_output_costs(conn)
        create_output_duals(conn)
        create_output_capacitybyperiodtech(conn)
        conn.close()
        return
