'''
This file has the objetive of make a wavelength sweep for a core with preset features
'''

import time
import numpy as np
from pdPythonLib import *
from datetime import datetime
from simulation_run import *
from core_profile_index_builder import *
from time_wind_simulation import *

# Get the current date and time
current_time = datetime.now()

# Convert the date and time to a string
time_string = current_time.strftime("%Y-%m-%d_%H-%M-%S")

results_file = 'core5_TA-TI_1550-1600nm' + '.csv'  # MODIFY
f = open(results_file, 'w')
fimmap = pdApp()
fimmap.StartApp('C:\\Program Files\\PhotonD\\Fimmwave\\bin64\\fimmwave.exe', 5101)

# MODIFY DEPENDING ON PLACE OF WORKING
# from work
test_dir = 'D:\\OneDrive UPV\\OneDrive - UPV\PhD-m\\2023-2024\\FiberDesin_PhotonD\\FOdesign_optimization'
# from personal computer
# test_dir = 'C:\\Users\\Mario\\OneDrive - UPV\PhD-m\\2023-2024\\FiberDesin_PhotonD\\FOdesign_optimization'

fiber_profile = ProfileIndexBuilder(fimmap)
fiber_profile.create_fimm_project('test', test_dir)
fiber_profile.add_moduleFWG('Module 1')
fiber_profile.set_material_db(test_dir, '\\refbase_2.mat')
dev = "app.subnodes[1].subnodes[1]"

## variation of input parameters MODIFY
# Defines the ranges for each parameter
a1 = 4.39
a2 = 3.03
a3 = 2.93
a4 = 30

dop_a1 = 0.1
dop_a2 = 0
dop_a3 = 0.1
dop_a4 = 0

alpha_a1 = 1
alpha_a2 = 0
alpha_a3 = 0
alpha_a4 = 0

# these variables define the number of steps in terms of scaling factor
number_steps = 100
param_Name = ["lambda"]
lam_s = 1.50
lam_e = 1.60
steps = np.linspace(lam_s, lam_e, number_steps)

# number of variable input parameters
p = 1 # wavelength is +1
# number of modes to analyze
n_m = 2
# creating variable to store the result (variable parameters)
data_scan = np.zeros((number_steps, n_m * 9 + p))  # 9-> max output of fiber_profile.mode_data()
elapsed_time = np.zeros(number_steps)

# simulation
experiment = SimulationRun(fimmap)
experiment.solver_config('GFS Fiber Solver')

param_Scan = {"beta": True, "neff": True, "a_eff": True, "alpha": True, "dispersion": True, "isLeaky": True,
              "neffg": True, "fillFac": True, "gammaE": True}

header = (
    ['wavelength(nm)',
     "beta (Real) mode 1", "neff (Real) mode 1", "a_eff mode 1", "alpha mode 1", "dispersion mode 1", "isLeaky mode 1",
     "neffg mode 1", "fillFac mode 1", "gammaE mode 1",
     "beta (Real) mode 2", "neff (Real) mode 2", "a_eff mode 2", "alpha mode 2", "dispersion mode 2", "isLeaky mode 2",
     "neffg mode 2", "fillFac mode 2", "gammaE mode 2"])

# showing the approximate simulation time
# under construction

# build the core
sizes = [a1, a2, a3, a4]
dop_perct = [dop_a1, dop_a2, dop_a3, dop_a4]
profile_type = ['Linear', 'Constant', 'Constant', 'Constant']
materials = ['GeO2-SiO2', 'SiO2', 'F-SiO2_1', 'SiO2']
alphas = [alpha_a1, alpha_a1, alpha_a3, alpha_a4]
n_steps = 50  # 2 for constant
fiber_profile.delete_layers()
fiber_profile.builder_profile(dev, sizes, dop_perct, profile_type, materials, alphas, n_steps)

try:
    # Iterate over all scaling values
    for i, wavelength in enumerate(steps):
        # Record the start time
        start_time = time.time()
        # setting the work wavelength
        fiber_profile.set_wavelength(dev, wavelength)
        # running simulation
        data_mode1 = experiment.simulate(param_Scan, mode='1')
        # running simulation mode 2
        data_mode2 = experiment.simulate(param_Scan, mode='3')

        data = np.hstack((data_mode1, data_mode2))

        data_scan[i, p:] = list(data)
        data_scan[i, 0:p] = [wavelength]
        # Record the end time
        end_time = time.time()
        # Calculate the elapsed time
        elapsed_time[i] = np.round(end_time - start_time,3)
        print("Simulation goes for: " + str(
            100 * i / number_steps) + ' %' + f" It took: {elapsed_time[i]} seconds")

except Exception as e:
    # Handle the exception
    print(f'An error occurred in the for loop: {str(e)}')
finally:
    data_scan = data_scan.astype('float')
    # add the new row to the top of the array
    data_scan = np.vstack((header, data_scan))

    for element in data_scan:
        f.write(','.join(element) + '\n')

    f.close()

    del fimmap
    print('DONE')
    print(f'The average simulation time was: {np.round(np.average(elapsed_time),2)} seconds')
    elapsed_time_h = np.round(np.sum(elapsed_time) / 3600, 2)
    print(f'The total simulation time was: {elapsed_time_h} hours')
