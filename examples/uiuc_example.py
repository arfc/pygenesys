# So the database can be saved in the location from which
# the command is called.
import os
curr_dir = os.path.dirname(__file__)


# Simulation metadata goes here
database_filename = 'uiuc_db.sqlite'  # where the database will be written
scenario_name = 'test'
start_year = 2021  # the first year optimized by the model
end_year = 2035  # the last year optimized by the model
N_years = 15  # the number of years optimized by the model
N_seasons = 4  # the number of "seasons" in the model
N_hours = 24  # the number of hours in a day

# Optional parameters
reserve_margin = {'UIUC':0.15}  # fraction of excess capacity to ensure reliability
discount_rate = 0.05  # The discount rate applied globally.

demands_list = []
resources_list = []
emissions_list = []

# Import demand commodities
from pygenesys.commodity.demand import ELC_DEMAND, STM_DEMAND, CW_DEMAND
from pygenesys.commodity.demand import TRANSPORT

# Add demand forecast
ELC_DEMAND.add_demand(region='UIUC',
                      init_demand=445.87,
                      start_year=start_year,
                      end_year=end_year,
                      N_years=N_years,
                      growth_rate=0.01,
                      growth_method='linear')
STM_DEMAND.add_demand(region='UIUC',
                      init_demand=505.51,
                      start_year=start_year,
                      end_year=end_year,
                      N_years=N_years,
                      growth_rate=0.01,
                      growth_method='linear')
CW_DEMAND.add_demand(region='UIUC',
                     init_demand=83.848,
                     start_year=start_year,
                     end_year=end_year,
                     N_years=N_years,
                     growth_rate=0.01,
                     growth_method='linear')

# Set demand distributions, import data
from pygenesys.data.library import (campus_elc_demand,
                                    campus_stm_demand,
                                    campus_cw_demand)
ELC_DEMAND.set_distribution(region='UIUC',
                            data=campus_elc_demand,
                            n_seasons=N_seasons,
                            n_hours=N_hours)
STM_DEMAND.set_distribution(region='UIUC',
                            data=campus_stm_demand,
                            n_seasons=N_seasons,
                            n_hours=N_hours)
CW_DEMAND.set_distribution(region='UIUC',
                           data=campus_cw_demand,
                           n_seasons=N_seasons,
                           n_hours=N_hours)


# Import transmission technologies, set regions, import input commodities
from pygenesys.technology.transmission import STM_TUNNEL, TRANSMISSION, CW_PIPES
from pygenesys.commodity.resource import (electricity,
                                          steam,
                                          chilled_water,
                                          nuclear_steam,
                                          ethos)
STM_TUNNEL.add_regional_data(region='UIUC',
                             input_comm=[steam, nuclear_steam],
                             output_comm=STM_DEMAND,
                             efficiency=1.0,
                             tech_lifetime=1000,)
TRANSMISSION.add_regional_data(region='UIUC',
                               input_comm=electricity,
                               output_comm=ELC_DEMAND,
                               efficiency=1.0,
                               tech_lifetime=1000,)
CW_PIPES.add_regional_data(region='UIUC',
                           input_comm=chilled_water,
                           output_comm=CW_DEMAND,
                           efficiency=1.0,
                           tech_lifetime=1000,)

# Import technologies that generate electricity
from pygenesys.technology.electric import SOLAR_FARM, WIND_FARM, IMP_ELC
from pygenesys.technology.electric import NUCLEAR_TB, ABBOTT_TB

# Import emissions
from pygenesys.commodity.emissions import co2eq


# Import capacity factor data
from pygenesys.data.library import solarfarm_data, railsplitter_data
from pygenesys.utils.tsprocess import choose_distribution_method

# Calculate the capacity factor distributions
method = choose_distribution_method(N_seasons, N_hours)
solar_cf = method(solarfarm_data, N_seasons, N_hours, kind='cf')
wind_cf = method(railsplitter_data, N_seasons, N_hours, kind='cf')

# Add regional data
SOLAR_FARM.add_regional_data(region='UIUC',
                             input_comm=ethos,
                             output_comm=electricity,
                             efficiency=1.0,
                             tech_lifetime=25,
                             loan_lifetime=10,
                             capacity_factor_tech=solar_cf,
                             existing={2016:4.86},
                             emissions={co2eq:4.8e-5})
WIND_FARM.add_regional_data(region='UIUC',
                            input_comm=ethos,
                            output_comm=electricity,
                            efficiency=1.0,
                            tech_lifetime=25,
                            loan_lifetime=10,
                            capacity_factor_tech=wind_cf,
                            existing={2016:8.7},
                            emissions={co2eq:1.1e-5})
IMP_ELC.add_regional_data(region='UIUC',
                          input_comm=ethos,
                          output_comm=electricity,
                          efficiency=1.0,
                          tech_lifetime=1000,
                          )
NUCLEAR_TB.add_regional_data(region='UIUC',
                             input_comm=nuclear_steam,
                             output_comm=electricity,
                             efficiency=0.33,
                             tech_lifetime=1000,
                             )
ABBOTT_TB.add_regional_data(region='UIUC',
                            input_comm=steam,
                            output_comm=electricity,
                            efficiency=0.4,
                            tech_lifetime=1000,
                            )
# Import thermal technologies
from pygenesys.technology.thermal import ABBOTT, NUCLEAR_THM, CWS

ABBOTT.add_regional_data(region='UIUC',
                         input_comm=ethos,
                         output_comm=steam,
                         efficiency=1.00,
                         tech_lifetime=40,
                         loan_lifetime=25,
                         capacity_factor_tech=0.57,
                         emissions={co2eq:5.7e-4})
NUCLEAR_THM.add_regional_data(region='UIUC',
                              input_comm=ethos,
                              output_comm=nuclear_steam,
                              efficiency=1.00,
                              tech_lifetime=60,
                              loan_lifetime=25,
                              capacity_factor_tech=0.93,
                              emissions={co2eq:1.2e-5})

from pygenesys.data.library import cws_data, tes_data
cws_cf = method(cws_data, N_seasons, N_hours, kind='cf')
tes_cf = method(tes_data, N_seasons, N_hours, kind='cf')

CWS.add_regional_data(region='UIUC',
                      input_comm=electricity,
                      output_comm=chilled_water,
                      efficiency=1.467,
                      tech_lifetime=40,
                      loan_lifetime=20,
                      capacity_factor_tech=cws_cf,
                      )


demands_list = [ELC_DEMAND, STM_DEMAND, CW_DEMAND]
resources_list = [electricity, steam, ethos, nuclear_steam, chilled_water]
emissions_list = [co2eq]

if __name__ == "__main__":
    import numpy as np

    horizon = np.linspace(start_year, end_year, N_years).astype('int')
    # print(horizon)

    import matplotlib.pyplot as plt
    plt.style.use('ggplot')

    # plt.plot(ELC_DEMAND.demand['UIUC'], label='exponential')
    # plt.ylim(0,520)
    # plt.legend()
    # plt.show()
    #
    # plt.plot(STM_DEMAND.distribution['UIUC'])
    # plt.plot(ELC_DEMAND.distribution['UIUC'])
    # plt.plot(CW_DEMAND.distribution['UIUC'])
    # plt.show()
