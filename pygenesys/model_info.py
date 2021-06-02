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

        time_horizon = np.arange(self.start_year,
                                 (self.end_year+1),
                                 self.year_step)

        return time_horizon


    def _calculate_seg_frac(self):
        """
        Calculates the fraction of a year represented
        by each time slice.
        Defines the values for the "SegFrac" table
        in the Temoa database.
        """

        seg_frac = 1/(self.N_seasons*self.N_hours)

        return seg_frac


    def _establish_connection(self):
        conn = None
        try:
            conn = sqlite3.connect(self.output_db)
        except:
            print("Database connection failed. Writing to sql file instead.")

        return conn


    def _write_sqlite_database(self):
        """
        Writes model info directly to a sqlite database.
        """

        conn = self._establish_connection()
        cursor = conn.cursor()

        # create fundamental tables
        cursor.execute(create_time_periods())
        cursor.execute(create_time_period_labels())
        cursor.execute(create_time_period())


        return
