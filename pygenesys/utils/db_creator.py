
import itertools
import sqlite3


def establish_connection(output_db):
    """
    Establishes connection with sqlite3 database.
    If the file does not exist, it will be created.

    Parameters
    ----------
    output_db : string
        The full path to the SQLite database.

    Returns
    -------
    conn : sqlite3 connection
        An object used to interact with a specific SQLite
        database.
    """
    conn = None
    try:
        conn = sqlite3.connect(output_db)
    except BaseException:
        print("Database connection failed. Writing to sql file instead.")
        print("Warning: SQL writing has not been implemented.")

    return conn


def create_time_season(connector, N_seasons):
    """
    This function writes the "time_season" table to an sqlite
    database.

    Parameters
    ----------
    connector : sqlite3 connection object
        An object for connecting to a specific SQLite
        database.

    N_seasons : integer
        The seasonal resolution of the energy system model.

    Returns
    -------
    table_command : string
        The command for generating the "time_season" table.
    """

    cursor = connector.cursor()

    table_command = """CREATE TABLE "time_season" (
                    	"t_season"	text,
                    	PRIMARY KEY("t_season")
                    );"""
    insert_command = """
                     INSERT INTO "time_season" VALUES (?)
                     """

    seasons = [[f'S{i+1}'] for i in range(N_seasons)]

    cursor.execute(table_command)
    cursor.executemany(insert_command, seasons)
    connector.commit()

    return seasons


def create_time_periods(connector, future_years):
    """
    This function writes the time_periods table to an sqlite
    database. Only "future" time periods will be written.

    Parameters
    ----------
    connector : sqlite3 connection object
        An object for connecting to a specific SQLite
        database.

    future_years : list or array
        The yearly resolution of the energy system model.

    Returns
    -------
    table_command : string
        The command for generating the "time_periods" table.
    """

    table_command = """CREATE TABLE "time_periods" (
                    	"t_periods"	integer,
                    	"flag"	text,
                    	PRIMARY KEY("t_periods"),
                    	FOREIGN KEY("flag") REFERENCES "time_period_labels"("t_period_labels")
                    );"""
    insert_command = """
                     INSERT INTO "time_periods" VALUES(?,?)
                     """

    time_horizon = [(int(year), 'f') for year in future_years]
    # set boundary year
    time_horizon.append((int(future_years[-1] + 1), 'f'))
    cursor = connector.cursor()
    cursor.execute(table_command)
    cursor.executemany(insert_command, time_horizon)
    connector.commit()
    return table_command


def create_time_period_labels(connector):
    """
    This function writes the "time_period_labels" table to an sqlite
    database.

    Parameters
    ----------
    connector : sqlite3 connection object
        An object for connecting to a specific SQLite
        database.

    Returns
    -------
    table_command : string
        The command for generating the "time_period_labels" table.
    """

    table_command = """CREATE TABLE "time_period_labels" (
                	"t_period_labels"	text,
                	"t_period_labels_desc"	text,
                	PRIMARY KEY("t_period_labels")
                    );"""
    labels = [('e', 'existing vintages'), ('f', 'future vintages')]

    insert_command = """
                     INSERT INTO "time_period_labels" VALUES(?,?)
                     """

    cursor = connector.cursor()
    cursor.execute(table_command)
    cursor.executemany(insert_command, labels)
    connector.commit()

    return table_command


def create_time_of_day(connector, N_hours):
    """
    This function writes the "time_of_day" table to an sqlite
    database.

    Parameters
    ----------
    connector : sqlite3 connection object
        An object for connecting to a specific SQLite
        database.

    N_hours : integer
        The hourly resolution of the energy system model.

    Returns
    -------
    table_command : string
        The command for generating the "time_of_day" table.
    """

    table_command = """CREATE TABLE "time_of_day" (
                    	"t_day"	text,
                    	PRIMARY KEY("t_day")
                    );"""

    insert_command = """
                     INSERT INTO "time_of_day" VALUES (?)
                     """

    times_of_day = [[f'H{i+1}'] for i in range(N_hours)]

    cursor = connector.cursor()
    cursor.execute(table_command)
    cursor.executemany(insert_command, times_of_day)
    connector.commit()

    return times_of_day


def create_segfrac(connector, segfrac, seasons, hours):
    """
    Generates the "SegFrac" table for the Temoa database.
    This table defines what fraction of a year is represented
    by each time slice.

    Parameters
    ----------
    connector : sqlite3 connection object
        Used to connect to and write to an sqlite database.
    segfrac : float
        The fraction-of-a-year represented by each time slice.
    seasons : list
        The list of seasons in the simulation.
    hours : list
        The list of hours in the simulation.

    Returns
    -------
    table_command : string
        The command for generating the "SegFrac" table.
    """

    table_command = """CREATE TABLE "SegFrac" (
                    	"season_name"	text,
                    	"time_of_day_name"	text,
                    	"segfrac"	real CHECK("segfrac" >= 0 AND "segfrac" <= 1),
                    	"segfrac_notes"	text,
                    	PRIMARY KEY("season_name","time_of_day_name"),
                    	FOREIGN KEY("season_name") REFERENCES "time_season"("t_season"),
                    	FOREIGN KEY("time_of_day_name") REFERENCES "time_of_day"("t_day")
                    );"""
    insert_command = """
                     INSERT INTO "SegFrac" VALUES (?,?,?,?)
                     """
    time_slices = itertools.product(seasons, hours)
    entries = [(ts[0][0], ts[1][0], segfrac, 'fraction of year')
               for ts in time_slices]

    cursor = connector.cursor()
    cursor.execute(table_command)
    cursor.executemany(insert_command, entries)
    connector.commit()

    return table_command


def create_commodity_labels(connector):
    """
    Writes a ``commodity_labels`` table to an SQLite database.

    Parameters
    ----------
    connector : sqlite3 connection object
        Used to connect to and write to an sqlite database.

    Returns
    -------
    table_command : string
        The command for generating the "commodity_labels" table.
    """
    table_command = """CREATE TABLE "commodity_labels" (
                       "comm_labels"	text,
                       "comm_labels_desc"	text,
                       PRIMARY KEY("comm_labels")
                    );
                    """

    insert_command = """
                     INSERT INTO "commodity_labels" VALUES (?,?)
                     """
    labels = [("p", "physical commodity"),
              ("d", "demand commodity"), ("e", "emissions commodity")]

    cursor = connector.cursor()
    cursor.execute(table_command)
    cursor.executemany(insert_command, labels)
    connector.commit()

    return


def create_commodities(connector, comm_data):
    """
    Writes a ``commodities`` table to an SQLite database.

    Parameters
    ----------
    connector : sqlite3 connection object
        Used to connect to and write to an sqlite database.

    comm_data : dictionary
        A dictionary of Commodity objects with keys
        * demand
        * resources
        * emissions

    Returns
    -------
    table_command : string
        The command for generating the "commodities" table.
    """
    table_command = """CREATE TABLE "commodities" (
                    	"comm_name"	text,
                    	"flag"	text,
                    	"comm_desc"	text,
                    	PRIMARY KEY("comm_name"),
                    	FOREIGN KEY("flag") REFERENCES "commodity_labels"("comm_labels")
                    );"""
    insert_command = """
                     INSERT INTO "commodities" VALUES(?,?,?)
                     """
    demand_entries = [comm._db_entry() for comm in comm_data['demand']]
    resource_entries = [comm._db_entry() for comm in comm_data['resources']]
    emission_entries = [comm._db_entry() for comm in comm_data['emissions']]

    labels = demand_entries + resource_entries + emission_entries

    cursor = connector.cursor()
    cursor.execute(table_command)
    cursor.executemany(insert_command, labels)
    connector.commit()

    return table_command


def create_regions(connector, regions):
    """
    Writes a ``regions`` table to an SQLite database.

    Parameters
    ----------
    connector : sqlite3 connection object
        Used to connect to and write to an sqlite database.

    regions : list
        A list of strings containing the unique regions in the
        model.

    Returns
    -------
    table_command : string
        The command for generating the "regions" table.
    """
    table_command = """CREATE TABLE "regions" (
                    	"regions"	TEXT,
                    	"region_note"	TEXT,
                    	PRIMARY KEY("regions")
                    );"""
    insert_command = """
                     INSERT INTO "regions" VALUES (?,?)
                     """
    labels = [(r, '') for r in regions]

    cursor = connector.cursor()
    cursor.execute(table_command)
    cursor.executemany(insert_command, labels)
    connector.commit()

    return


def create_demand_table(connector, demand_list, years):
    """
    Writes a ``demand`` table to an SQLite database.

    Parameters
    ----------
    connector : sqlite3 connection object
        Used to connect to and write to an sqlite database.

    demand_list : list
        A list of DemandCommodity objects.

    years : list or array
        A list of the years in the model simulation.

    Returns
    -------
    table_command : string
        The command for generating the "demand" table.
    """
    table_command = """CREATE TABLE "Demand" (
                    	"regions"	text,
                    	"periods"	integer,
                    	"demand_comm"	text,
                    	"demand"	real,
                    	"demand_units"	text,
                    	"demand_notes"	text,
                    	PRIMARY KEY("regions","periods","demand_comm"),
                    	FOREIGN KEY("periods") REFERENCES "time_periods"("t_periods"),
                    	FOREIGN KEY("demand_comm") REFERENCES "commodities"("comm_name")
                    );"""

    insert_command = """
                    INSERT INTO "Demand" VALUES (?,?,?,?,?,?)
    """

    cursor = connector.cursor()
    cursor.execute(table_command)
    # loops over each commodity (electricity, steam, h2, etc.)
    for demand_comm in demand_list:
        demand_dict = demand_comm.demand
        # loops over each region where the commodity is defined
        for region in demand_dict:
            data = demand_dict[region]
            db_entry = [(region,
                         int(y),
                         demand_comm.comm_name,
                         d,
                         demand_comm.units,
                         '') for d, y in zip(data, years)]
            cursor.executemany(insert_command, db_entry)

    connector.commit()
    return table_command


def create_demand_specific_distribution(connector,
                                        demand_list,
                                        seasons,
                                        hours):
    """
    This function writes the ``DemandSpecificDistribution`` table
    in Temoa.

    Parameters
    ----------
    connector : sqlite3 connection object
        Used to connect to and write to an sqlite database.
    demand_list : list of DemandCommodity objects
        The list of objects that store information about
        the demand commodities for the Temoa simulation.
    seasons : list
        The list of seasons in the simulation.
    hours : list
        The list of hours in the simulation.

    Returns
    -------
    table_command : string
        The command for creating the SQLite table.
    """
    table_command = """CREATE TABLE "DemandSpecificDistribution" (
                	"regions"	text,
                	"season_name"	text,
                	"time_of_day_name"	text,
                	"demand_name"	text,
                	"dds"	real CHECK("dds" >= 0 AND "dds" <= 1),
                	"dds_notes"	text,
                	PRIMARY KEY("regions","season_name","time_of_day_name","demand_name"),
                	FOREIGN KEY("season_name") REFERENCES "time_season"("t_season"),
                	FOREIGN KEY("time_of_day_name") REFERENCES "time_of_day"("t_day"),
                	FOREIGN KEY("demand_name") REFERENCES "commodities"("comm_name")
                    );"""
    insert_command = """
                     INSERT INTO "DemandSpecificDistribution" VALUES (?,?,?,?,?,?)
                     """

    cursor = connector.cursor()
    cursor.execute(table_command)

    for demand_comm in demand_list:
        time_slices = itertools.product(hours, seasons)
        demand_dict = demand_comm.distribution
        # loops over each region where the commodity is defined
        for region in demand_dict:
            data = demand_dict[region]
            db_entry = [
                (region,
                 ts[0][0],
                    ts[1][0],
                    demand_comm.comm_name,
                    d,
                    demand_comm.units) for d,
                ts in zip(
                    data,
                    time_slices)]
            cursor.executemany(insert_command, db_entry)
    connector.commit()
    return table_command


def create_technology_labels(connector):
    """
    Writes a ``technology_labels`` table to an SQLite database.

    Parameters
    ----------
    connector : sqlite3 connection object
        Used to connect to and write to an sqlite database.

    Returns
    -------
    table_command : string
        The command for generating the "commodity_labels" table.
    """
    table_command = """CREATE TABLE "technology_labels" (
    	"tech_labels"	text,
    	"tech_labels_desc"	text,
    	PRIMARY KEY("tech_labels")
    );
                    """

    insert_command = """
                     INSERT INTO "technology_labels" VALUES (?,?)
                     """
    labels = [("p", "production technology"),
              ("pb", "baseload production technology"),
              ("ps", "storage production technology"),
              ("r", "resource technology")]

    cursor = connector.cursor()
    cursor.execute(table_command)
    cursor.executemany(insert_command, labels)
    connector.commit()

    return


def create_sectors(connector, sector_list):

    table_command = """
                    CREATE TABLE "sector_labels" (
                    "sector"	text,
                    PRIMARY KEY("sector")
                    );"""

    insert_command = """
                     INSERT INTO "sector_labels" VALUES (?)
                     """

    sectors = [[s] for s in sector_list]

    cursor = connector.cursor()
    cursor.execute(table_command)
    cursor.executemany(insert_command, sectors)
    connector.commit()

    return


def create_technologies(connector, technology_list):
    """
    Creates the ``technologies`` table in Temoa.

    Parameters
    ----------
    connector : sqlite connector
        The connection to an sqlite database

    technology_list : list of ``Technology`` objects
        All of the technologies initialized in the input file
    """

    table_command = """
                    CREATE TABLE "technologies" (
                    "tech"	text,
                    "flag"	text,
                    "sector"	text,
                    "tech_desc"	text,
                    "tech_category"	text,
                    PRIMARY KEY("tech"),
                    FOREIGN KEY("flag") REFERENCES "technology_labels"("tech_labels"),
                    FOREIGN KEY("sector") REFERENCES "sector_labels"("sector")
                    );"""
    insert_command = """
                     INSERT INTO "technologies" VALUES (?,?,?,?,?)
                     """
    tech_entries = [tech._db_entry() for tech in technology_list]

    cursor = connector.cursor()
    cursor.execute(table_command)
    cursor.executemany(insert_command, tech_entries)
    connector.commit()

    return table_command


"""


def create_():
CREATE TABLE "tech_reserve" (
	"tech"	text,
	"notes"	text,
	PRIMARY KEY("tech")
);
return


def create_():
CREATE TABLE "tech_exchange" (
	"tech"	text,
	"notes"	TEXT,
	PRIMARY KEY("tech"),
	FOREIGN KEY("tech") REFERENCES "technologies"("tech")
);
return


def create_():
CREATE TABLE "tech_curtailment" (
	"tech"	text,
	"notes"	TEXT,
	PRIMARY KEY("tech"),
	FOREIGN KEY("tech") REFERENCES "technologies"("tech")
);
return


def create_():
CREATE TABLE "tech_flex" (
	"tech"	text,
	"notes"	TEXT,
	PRIMARY KEY("tech"),
	FOREIGN KEY("tech") REFERENCES "technologies"("tech")
);
return


def create_():
CREATE TABLE "tech_annual" (
	"tech"	text,
	"notes"	TEXT,
	PRIMARY KEY("tech"),
	FOREIGN KEY("tech") REFERENCES "technologies"("tech")
);
return



def create_():
CREATE TABLE "groups" (
	"group_name"	text,
	"notes"	text,
	PRIMARY KEY("group_name")
);
return

def create_():

def create_():
CREATE TABLE "TechOutputSplit" (
	"regions"	TEXT,
	"periods"	integer,
	"tech"	TEXT,
	"output_comm"	text,
	"to_split"	real,
	"to_split_notes"	text,
	PRIMARY KEY("regions","periods","tech","output_comm"),
	FOREIGN KEY("output_comm") REFERENCES "commodities"("comm_name"),
	FOREIGN KEY("periods") REFERENCES "time_periods"("t_periods"),
	FOREIGN KEY("tech") REFERENCES "technologies"("tech")
);
return

def create_():
CREATE TABLE "TechInputSplit" (
	"regions"	TEXT,
	"periods"	integer,
	"input_comm"	text,
	"tech"	text,
	"ti_split"	real,
	"ti_split_notes"	text,
	PRIMARY KEY("regions","periods","input_comm","tech"),
	FOREIGN KEY("tech") REFERENCES "technologies"("tech"),
	FOREIGN KEY("input_comm") REFERENCES "commodities"("comm_name"),
	FOREIGN KEY("periods") REFERENCES "time_periods"("t_periods")
);
return

def create_():
CREATE TABLE "StorageDuration" (
	"regions"	text,
	"tech"	text,
	"duration"	real,
	"duration_notes"	text,
	PRIMARY KEY("regions","tech")
);
return



def create_():
CREATE TABLE "PlanningReserveMargin" (
	`regions`	text,
	`reserve_margin`	REAL,
	PRIMARY KEY(regions),
	FOREIGN KEY(`regions`) REFERENCES regions
);
return

def create_():
CREATE TABLE "Output_V_Capacity" (
	"regions"	text,
	"scenario"	text,
	"sector"	text,
	"tech"	text,
	"vintage"	integer,
	"capacity"	real,
	PRIMARY KEY("regions","scenario","tech","vintage"),
	FOREIGN KEY("sector") REFERENCES "sector_labels"("sector"),
	FOREIGN KEY("tech") REFERENCES "technologies"("tech"),
	FOREIGN KEY("vintage") REFERENCES "time_periods"("t_periods")
);
return

def create_():
CREATE TABLE "Output_VFlow_Out" (
	"regions"	text,
	"scenario"	text,
	"sector"	text,
	"t_periods"	integer,
	"t_season"	text,
	"t_day"	text,
	"input_comm"	text,
	"tech"	text,
	"vintage"	integer,
	"output_comm"	text,
	"vflow_out"	real,
	PRIMARY KEY("regions","scenario","t_periods","t_season","t_day","input_comm","tech","vintage","output_comm"),
	FOREIGN KEY("output_comm") REFERENCES "commodities"("comm_name"),
	FOREIGN KEY("t_periods") REFERENCES "time_periods"("t_periods"),
	FOREIGN KEY("vintage") REFERENCES "time_periods"("t_periods"),
	FOREIGN KEY("t_season") REFERENCES "time_periods"("t_periods"),
	FOREIGN KEY("tech") REFERENCES "technologies"("tech"),
	FOREIGN KEY("sector") REFERENCES "sector_labels"("sector"),
	FOREIGN KEY("t_day") REFERENCES "time_of_day"("t_day"),
	FOREIGN KEY("input_comm") REFERENCES "commodities"("comm_name")
);
return

def create_():
CREATE TABLE "Output_VFlow_In" (
	"regions"	text,
	"scenario"	text,
	"sector"	text,
	"t_periods"	integer,
	"t_season"	text,
	"t_day"	text,
	"input_comm"	text,
	"tech"	text,
	"vintage"	integer,
	"output_comm"	text,
	"vflow_in"	real,
	PRIMARY KEY("regions","scenario","t_periods","t_season","t_day","input_comm","tech","vintage","output_comm"),
	FOREIGN KEY("vintage") REFERENCES "time_periods"("t_periods"),
	FOREIGN KEY("output_comm") REFERENCES "commodities"("comm_name"),
	FOREIGN KEY("t_periods") REFERENCES "time_periods"("t_periods"),
	FOREIGN KEY("sector") REFERENCES "sector_labels"("sector"),
	FOREIGN KEY("t_season") REFERENCES "time_periods"("t_periods"),
	FOREIGN KEY("t_day") REFERENCES "time_of_day"("t_day"),
	FOREIGN KEY("input_comm") REFERENCES "commodities"("comm_name"),
	FOREIGN KEY("tech") REFERENCES "technologies"("tech")
);
return

def create_():
CREATE TABLE "Output_Objective" (
	"scenario"	text,
	"objective_name"	text,
	"total_system_cost"	real
);
return

def create_():
CREATE TABLE "Output_Emissions" (
	"regions"	text,
	"scenario"	text,
	"sector"	text,
	"t_periods"	integer,
	"emissions_comm"	text,
	"tech"	text,
	"vintage"	integer,
	"emissions"	real,
	PRIMARY KEY("regions","scenario","t_periods","emissions_comm","tech","vintage"),
	FOREIGN KEY("vintage") REFERENCES "time_periods"("t_periods"),
	FOREIGN KEY("emissions_comm") REFERENCES "EmissionActivity"("emis_comm"),
	FOREIGN KEY("tech") REFERENCES "technologies"("tech"),
	FOREIGN KEY("sector") REFERENCES "sector_labels"("sector"),
	FOREIGN KEY("t_periods") REFERENCES "time_periods"("t_periods")
);
return

def create_():
CREATE TABLE "Output_Curtailment" (
	"regions"	text,
	"scenario"	text,
	"sector"	text,
	"t_periods"	integer,
	"t_season"	text,
	"t_day"	text,
	"input_comm"	text,
	"tech"	text,
	"vintage"	integer,
	"output_comm"	text,
	"curtailment"	real,
	PRIMARY KEY("regions","scenario","t_periods","t_season","t_day","input_comm","tech","vintage","output_comm"),
	FOREIGN KEY("tech") REFERENCES "technologies"("tech"),
	FOREIGN KEY("vintage") REFERENCES "time_periods"("t_periods"),
	FOREIGN KEY("input_comm") REFERENCES "commodities"("comm_name"),
	FOREIGN KEY("output_comm") REFERENCES "commodities"("comm_name"),
	FOREIGN KEY("t_periods") REFERENCES "time_periods"("t_periods"),
	FOREIGN KEY("t_season") REFERENCES "time_periods"("t_periods"),
	FOREIGN KEY("t_day") REFERENCES "time_of_day"("t_day")
);
return

def create_():
CREATE TABLE "Output_Costs" (
	"regions"	text,
	"scenario"	text,
	"sector"	text,
	"output_name"	text,
	"tech"	text,
	"vintage"	integer,
	"output_cost"	real,
	PRIMARY KEY("regions","scenario","output_name","tech","vintage"),
	FOREIGN KEY("vintage") REFERENCES "time_periods"("t_periods"),
	FOREIGN KEY("sector") REFERENCES "sector_labels"("sector"),
	FOREIGN KEY("tech") REFERENCES "technologies"("tech")
);
return

def create_():
CREATE TABLE "Output_Duals" (
	"constraint_name"	text,
	"scenario"	text,
	"dual"	real,
	PRIMARY KEY("constraint_name","scenario")
);
return

def create_():
CREATE TABLE "Output_CapacityByPeriodAndTech" (
	"regions"	text,
	"scenario"	text,
	"sector"	text,
	"t_periods"	integer,
	"tech"	text,
	"capacity"	real,
	PRIMARY KEY("regions","scenario","t_periods","tech"),
	FOREIGN KEY("sector") REFERENCES "sector_labels"("sector"),
	FOREIGN KEY("t_periods") REFERENCES "time_periods"("t_periods"),
	FOREIGN KEY("tech") REFERENCES "technologies"("tech")
);
return

def create_():
CREATE TABLE "MyopicBaseyear" (
	"year"	real
	"notes"	text
);
return

def create_():
CREATE TABLE "MinGenGroupWeight" (
	"regions"	text,
	"tech"	text,
	"group_name"	text,
	"act_fraction"	REAL,
	"tech_desc"	text,
	PRIMARY KEY("tech","group_name","regions")
);
return

def create_():
CREATE TABLE "MinGenGroupTarget" (
	"regions"	text,
	"periods"	integer,
	"group_name"	text,
	"min_act_g"	real,
	"notes"	text,
	PRIMARY KEY("periods","group_name","regions")
);
return

def create_():
CREATE TABLE "MinCapacity" (
	"regions"	text,
	"periods"	integer,
	"tech"	text,
	"mincap"	real,
	"mincap_units"	text,
	"mincap_notes"	text,
	PRIMARY KEY("regions","periods","tech"),
	FOREIGN KEY("tech") REFERENCES "technologies"("tech"),
	FOREIGN KEY("periods") REFERENCES "time_periods"("t_periods")
);
return

def create_():
CREATE TABLE "MinActivity" (
	"regions"	text,
	"periods"	integer,
	"tech"	text,
	"minact"	real,
	"minact_units"	text,
	"minact_notes"	text,
	PRIMARY KEY("regions","periods","tech"),
	FOREIGN KEY("tech") REFERENCES "technologies"("tech"),
	FOREIGN KEY("periods") REFERENCES "time_periods"("t_periods")
);
return

def create_():
CREATE TABLE "MaxCapacity" (
	"regions"	text,
	"periods"	integer,
	"tech"	text,
	"maxcap"	real,
	"maxcap_units"	text,
	"maxcap_notes"	text,
	PRIMARY KEY("regions","periods","tech"),
	FOREIGN KEY("periods") REFERENCES "time_periods"("t_periods"),
	FOREIGN KEY("tech") REFERENCES "technologies"("tech")
);
return

def create_():
CREATE TABLE "MaxActivity" (
	"regions"	text,
	"periods"	integer,
	"tech"	text,
	"maxact"	real,
	"maxact_units"	text,
	"maxact_notes"	text,
	PRIMARY KEY("regions","periods","tech"),
	FOREIGN KEY("periods") REFERENCES "time_periods"("t_periods"),
	FOREIGN KEY("tech") REFERENCES "technologies"("tech")
);
return

def create_():
CREATE TABLE "LifetimeTech" (
	"regions"	text,
	"tech"	text,
	"life"	real,
	"life_notes"	text,
	PRIMARY KEY("regions","tech"),
	FOREIGN KEY("tech") REFERENCES "technologies"("tech")
);
return

def create_():
CREATE TABLE "LifetimeProcess" (
	"regions"	text,
	"tech"	text,
	"vintage"	integer,
	"life_process"	real,
	"life_process_notes"	text,
	PRIMARY KEY("regions","tech","vintage"),
	FOREIGN KEY("vintage") REFERENCES "time_periods"("t_periods"),
	FOREIGN KEY("tech") REFERENCES "technologies"("tech")
);
return

def create_():
CREATE TABLE "LifetimeLoanTech" (
	"regions"	text,
	"tech"	text,
	"loan"	real,
	"loan_notes"	text,
	PRIMARY KEY("regions","tech"),
	FOREIGN KEY("tech") REFERENCES "technologies"("tech")
);
return

def create_():
CREATE TABLE "GrowthRateSeed" (
	"regions"	text,
	"tech"	text,
	"growthrate_seed"	real,
	"growthrate_seed_units"	text,
	"growthrate_seed_notes"	text,
	PRIMARY KEY("regions","tech"),
	FOREIGN KEY("tech") REFERENCES "technologies"("tech")
);
return

def create_():
CREATE TABLE "GrowthRateMax" (
	"regions"	text,
	"tech"	text,
	"growthrate_max"	real,
	"growthrate_max_notes"	text,
	PRIMARY KEY("regions","tech"),
	FOREIGN KEY("tech") REFERENCES "technologies"("tech")
);
return

def create_():
CREATE TABLE "GlobalDiscountRate" (
	"rate"	real
);
return

def create_():
CREATE TABLE "ExistingCapacity" (
	"regions"	text,
	"tech"	text,
	"vintage"	integer,
	"exist_cap"	real,
	"exist_cap_units"	text,
	"exist_cap_notes"	text,
	PRIMARY KEY("regions","tech","vintage"),
	FOREIGN KEY("tech") REFERENCES "technologies"("tech"),
	FOREIGN KEY("vintage") REFERENCES "time_periods"("t_periods")
);
return

def create_():
CREATE TABLE "EmissionLimit" (
	"regions"	text,
	"periods"	integer,
	"emis_comm"	text,
	"emis_limit"	real,
	"emis_limit_units"	text,
	"emis_limit_notes"	text,
	PRIMARY KEY("periods","emis_comm"),
	FOREIGN KEY("periods") REFERENCES "time_periods"("t_periods"),
	FOREIGN KEY("emis_comm") REFERENCES "commodities"("comm_name")
);
return

def create_():
CREATE TABLE "EmissionActivity" (
	"regions"	text,
	"emis_comm"	text,
	"input_comm"	text,
	"tech"	text,
	"vintage"	integer,
	"output_comm"	text,
	"emis_act"	real,
	"emis_act_units"	text,
	"emis_act_notes"	text,
	PRIMARY KEY("regions","emis_comm","input_comm","tech","vintage","output_comm"),
	FOREIGN KEY("input_comm") REFERENCES "commodities"("comm_name"),
	FOREIGN KEY("tech") REFERENCES "technologies"("tech"),
	FOREIGN KEY("vintage") REFERENCES "time_periods"("t_periods"),
	FOREIGN KEY("output_comm") REFERENCES "commodities"("comm_name"),
	FOREIGN KEY("emis_comm") REFERENCES "commodities"("comm_name")
);
return

def create_():
CREATE TABLE "Efficiency" (
	"regions"	text,
	"input_comm"	text,
	"tech"	text,
	"vintage"	integer,
	"output_comm"	text,
	"efficiency"	real CHECK("efficiency" > 0),
	"eff_notes"	text,
	PRIMARY KEY("regions","input_comm","tech","vintage","output_comm"),
	FOREIGN KEY("output_comm") REFERENCES "commodities"("comm_name"),
	FOREIGN KEY("tech") REFERENCES "technologies"("tech"),
	FOREIGN KEY("vintage") REFERENCES "time_periods"("t_periods"),
	FOREIGN KEY("input_comm") REFERENCES "commodities"("comm_name")
);
return

def create_():
CREATE TABLE "DiscountRate" (
	"regions"	text,
	"tech"	text,
	"vintage"	integer,
	"tech_rate"	real,
	"tech_rate_notes"	text,
	PRIMARY KEY("regions","tech","vintage"),
	FOREIGN KEY("tech") REFERENCES "technologies"("tech"),
	FOREIGN KEY("vintage") REFERENCES "time_periods"("t_periods")
);
return




def create_():
CREATE TABLE "CostVariable" (
	"regions"	text NOT NULL,
	"periods"	integer NOT NULL,
	"tech"	text NOT NULL,
	"vintage"	integer NOT NULL,
	"cost_variable"	real,
	"cost_variable_units"	text,
	"cost_variable_notes"	text,
	PRIMARY KEY("regions","periods","tech","vintage"),
	FOREIGN KEY("tech") REFERENCES "technologies"("tech"),
	FOREIGN KEY("vintage") REFERENCES "time_periods"("t_periods"),
	FOREIGN KEY("periods") REFERENCES "time_periods"("t_periods")
);
return

def create_():
CREATE TABLE "CostInvest" (
	"regions"	text,
	"tech"	text,
	"vintage"	integer,
	"cost_invest"	real,
	"cost_invest_units"	text,
	"cost_invest_notes"	text,
	PRIMARY KEY("regions","tech","vintage"),
	FOREIGN KEY("tech") REFERENCES "technologies"("tech"),
	FOREIGN KEY("vintage") REFERENCES "time_periods"("t_periods")
);
return

def create_():
CREATE TABLE "CostFixed" (
	"regions"	text NOT NULL,
	"periods"	integer NOT NULL,
	"tech"	text NOT NULL,
	"vintage"	integer NOT NULL,
	"cost_fixed"	real,
	"cost_fixed_units"	text,
	"cost_fixed_notes"	text,
	PRIMARY KEY("regions","periods","tech","vintage"),
	FOREIGN KEY("tech") REFERENCES "technologies"("tech"),
	FOREIGN KEY("vintage") REFERENCES "time_periods"("t_periods"),
	FOREIGN KEY("periods") REFERENCES "time_periods"("t_periods")
);
return

def create_():
CREATE TABLE "CapacityToActivity" (
	"regions"	text,
	"tech"	text,
	"c2a"	real,
	"c2a_notes"	TEXT,
	PRIMARY KEY("regions","tech"),
	FOREIGN KEY("tech") REFERENCES "technologies"("tech")
);
return

def create_():
CREATE TABLE "CapacityFactorTech" (
	"regions"	text,
	"season_name"	text,
	"time_of_day_name"	text,
	"tech"	text,
	"cf_tech"	real CHECK("cf_tech" >= 0 AND "cf_tech" <= 1),
	"cf_tech_notes"	text,
	PRIMARY KEY("regions","season_name","time_of_day_name","tech"),
	FOREIGN KEY("season_name") REFERENCES "time_season"("t_season"),
	FOREIGN KEY("time_of_day_name") REFERENCES "time_of_day"("t_day"),
	FOREIGN KEY("tech") REFERENCES "technologies"("tech")
);
return

def create_():
CREATE TABLE "CapacityFactorProcess" (
	"regions"	text,
	"season_name"	text,
	"time_of_day_name"	text,
	"tech"	text,
	"vintage"	integer,
	"cf_process"	real CHECK("cf_process" >= 0 AND "cf_process" <= 1),
	"cf_process_notes"	text,
	PRIMARY KEY("regions","season_name","time_of_day_name","tech","vintage"),
	FOREIGN KEY("tech") REFERENCES "technologies"("tech"),
	FOREIGN KEY("season_name") REFERENCES "time_season"("t_season"),
	FOREIGN KEY("time_of_day_name") REFERENCES "time_of_day"("t_day")
);
return

def create_():
CREATE TABLE "CapacityCredit" (
	"regions"	text,
	"periods"	integer,
	"tech"	text,
	"vintage" integer,
	"cf_tech"	real CHECK("cf_tech" >= 0 AND "cf_tech" <= 1),
	"cf_tech_notes"	text,
	PRIMARY KEY("regions","periods","tech","vintage")
);
return

def create_():
CREATE TABLE "MaxResource" (
	"regions"	text,
	"tech"	text,
	"maxres"	real,
	"maxres_units"	text,
	"maxres_notes"	text,
	FOREIGN KEY("tech") REFERENCES "technologies"("tech"),
	PRIMARY KEY("regions","tech")
);
return
"""
