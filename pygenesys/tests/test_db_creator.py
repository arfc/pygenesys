from pygenesys.db_creator import *
import os

curr_dir = os.path.dirname(__file__)
test_db = curr_dir+'/test_db.sqlite'
N_seasons = 4
N_hours = 24
start_year = 2020
end_year = 2050
year_step = 5
seasons = [[f'S{i+1}'] for i in range(N_seasons)]
periods = [(year, 'f') for year in range(self.start_year,
                                         self.end_year+1,
                                         self.year_step)]

def test_establish_connection():
    conn = establish_connection(test_db)

    assert(conn is not None)

    conn.close()
    os.remove(test_db)
    return


def test_create_time_season():

    # set up
    conn = establish_connection(test_db)
    func_seasons = create_time_season(conn, N_seasons)
    cursor = conn.cursor()
    table_data = list(cursor.execute("SELECT * FROM time_season"))
    conn.close()

    # tests
    assert(len(table_data) == N_seasons)
    assert(func_seasons == seasons)

    # clean up
    os.remove(test_db)
    return table_data


def test_create_time_period_labels():
    # set up
    conn = establish_connection(test_db)
    create_time_period_labels(conn)
    cursor = conn.cursor()
    table_data = list(cursor.execute("SELECT * FROM time_period_labels"))
    conn.close()

    N_labels = 2
    # tests
    assert(len(table_data) == N_labels)

    os.remove(test_db)
    return


def test_create_time_periods():
    # set up
    conn = establish_connection(test_db)
    create_time_periods(conn, periods)
    cursor = conn.cursor()
    table_data = list(cursor.execute("SELECT * FROM time_periods"))
    conn.close()

    # tests
    assert(len(table_data) == N_labels)

    os.remove(test_db)
    return
