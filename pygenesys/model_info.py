import numpy as np
import sqlite3
from pygenesys.db_creator import *


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
                 year_step,
                 N_seasons,
                 N_hours):
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
                * 1; there are no seasonal differences
                * 4; spring,summer,fall,winter
                * 365; full year, daily resolution
        N_hours : int
            The number of hours in the simulation. Several values
            are acceptable. E.g.
                * 1; there is no daily variation
                * 2; diurnal variation, step function
                * 24; full day, hourly resolution
        """

        self.output_db = output_db
        self.scenario_name = scenario_name
        self.start_year = start_year
        self.end_year = end_year
        self.year_step = year_step
        self.N_seasons = N_seasons
        self.N_hours = N_hours

        # derived quantities
        self.time_horizon = self._calculate_time_horizon()
        self.seg_frac = self._calculate_seg_frac()

        return

    def _calculate_time_horizon(self):
        """
        Calculates the complete simulation time horizon.
        Defines the "future" time periods in the Temoa
        database.
        """

        time_horizon = [(year, 'f') for year in range(self.start_year,
                                                      (self.end_year +
                                                       self.year_step + 1),
                                                      self.year_step)]
        return time_horizon

    def _calculate_seg_frac(self):
        """
        Calculates the fraction of a year represented
        by each time slice.
        Defines the values for the "SegFrac" table
        in the Temoa database.
        """

        seg_frac = 1 / (self.N_seasons * self.N_hours)

        return seg_frac

    def _write_sqlite_database(self):
        """
        Writes model info directly to a sqlite database.
        """

        conn = establish_connection(self.output_db)

        # create fundamental tables
        seasons = create_time_season(conn, self.N_seasons)
        create_time_period_labels(conn)
        create_time_periods(conn, self.time_horizon)
        time_slices = create_time_of_day(conn, self.N_hours)
        create_segfrac(conn, self.seg_frac, seasons, time_slices)

        conn.close()
        return
