'''

Type of Materiales: 'GeO2-SiO2', 'SiO2', 'F-SiO2_1', 'F-SiO2_2'
Type of Regions: 'Constant', 'Linear' | 'Graded' (alpha = 1, alpha > 0 & alpha != 1), 'Raised cosine' (alpha = 1), 'Custom function' (not implemented yet)

'''

import time
import os

from pdPythonLib import *
from datetime import datetime
from simulation_run import *
from fiber.core_profile_index_builder import ProfileIndexBuilder


# Get the current date and time
current_time = datetime.now()

# Convert the date and time to a string
time_string = current_time.strftime("%Y-%m-%d_%H-%M-%S")

# build profile with index-profile:
type_index_profile = 'triangular with trench F-SiO2_2 and ring'

results_file = type_index_profile + time_string +'ALL COMB' +'.csv'  # MODIFY
# Open the CSV file in written mode
f = open(results_file, 'w')

fimmap = pdApp()
fimmap.StartApp('C:\\Program Files\\PhotonD\\Fimmwave\\bin64\\fimmwave.exe', 5101)


# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Get the root directory by removing the last folder
work_dir = os.path.dirname(script_dir)

fiber_profile = ProfileIndexBuilder(fimmap)
fiber_profile.create_fimm_project('test', work_dir)
fiber_profile.add_moduleFWG('Module 1')
fiber_profile.set_material_db(work_dir, '\\fimmwave\\refbase_2.mat')

print(work_dir, '\\fimmwave\\refbase_2.mat')
dev = "app.subnodes[1].subnodes[1]"

## variation of input parameters MODIFY
# Defines the ranges for each parameter
a1 = np.linspace(1.5, 5, 7)
a2 = np.linspace(1.5, 5, 7)
a3 = np.linspace(1.5, 5, 7)
a4 = np.linspace(25, 25, 1)
a5 = np.linspace(25, 25, 1)

dop_a1 = np.linspace(0.01, 0.1, 5)
dop_a2 = np.linspace(0, 0, 1)
dop_a3 = np.linspace(0, 0.08, 5)
dop_a4 = np.linspace(0, 0, 1)
dop_a5 = np.linspace(0, 0, 1)

alpha_a1 = np.linspace(1, 1, 1)
alpha_a2 = 0
alpha_a3 = 0
alpha_a4 = 0
alpha_a5 = 0

n_steps = np.linspace(11, 11, 1)

# Define wavelength range
lam_s = 1.53
lam_e = 1.57
wavelength_steps = np.linspace(lam_s, lam_e, 5)

# number of variable input parameters
p = 13
# creating variable to store the result (variable parameters)
steps = len(a1) * len(a2) * len(a3) * len(a4) * len(dop_a1) * len(dop_a2) * len(dop_a3) * len(alpha_a1)* len(wavelength_steps)*len(n_steps) # MODIFY
data_scan = np.zeros((steps, 2 * 9 + p))  # 9-> max output of fiber_profile.mode_data(), 3* because is three modes
elapsed_time = np.zeros(steps)
i = 0

# simulation
experiment = SimulationRun(fimmap)
experiment.solver_config('GFS Fiber Solver')

param_Scan = {"beta": True, "neff": True, "a_eff": True, "alpha": True, "dispersion": True, "isLeaky": True,
              "neffg": True, "fillFac": True, "gammaE": True}

header = (
    ['a1(um)', 'a2(um)', 'a3(um)', 'a4(um)', 'a5(um)',
     'n1 dopant(%)', 'n2 dopant(%)', 'n3 dopant(%)', 'n4 dopant(%)', 'n5 dopant(%)', 'alpha a1', 'wavelength', 'n steps',
     "beta (Real) mode 1", "neff (Real) mode 1", "a_eff mode 1", "alpha mode 1", "dispersion mode 1", "isLeaky mode 1",
     "neffg mode 1", "fillFac mode 1", "gammaE mode 1",
     "beta (Real) mode 2", "neff (Real) mode 2", "a_eff mode 2", "alpha mode 2", "dispersion mode 2", "isLeaky mode 2",
     "neffg mode 2", "fillFac mode 2", "gammaE mode 2"])
'''
     "beta (Real) mode 3", "neff (Real) mode 3", "a_eff mode 3", "alpha mode 3", "dispersion mode 3", "isLeaky mode 3",
     "neffg mode 3", "fillFac mode 3", "gammaE mode 3"])'''

# prof = 'steps', 'triangular', 'graded', 'raised cosine'

try:
    # Iterate over all combinations of parameters
    for a1_val in a1:
        for a2_val in a2:
            for a3_val in a3:
                for a4_val in a4:
                    for a5_val in a5:
                        for a1_dopant_val in dop_a1:
                            for a2_dopant_val in dop_a2:
                                #for a3_dopant_val in dop_a3:
                                # Generate a3_dopant_val dynamically from 0 to a1_dopant_val in 10 steps
                                for a3_dopant_val in np.linspace(0, a1_dopant_val, 8):
                                    for a4_dopant_val in dop_a4:
                                        for a5_dopant_val in dop_a5:
                                            for a1_alpha_val in alpha_a1:
                                                for wavelength_steps_val in wavelength_steps:
                                                    for n_steps_val in n_steps:
                                                        # Record the start time
                                                        start_time = time.time()
                                                        # Convertir truncando los decimales
                                                        n_steps_val= n_steps_val.astype(int)

                                                        sizes = [a1_val, a2_val, a3_val, a4_val, a5_val]

                                                        dop_perct = [a1_dopant_val, a2_dopant_val, a3_dopant_val,
                                                                     a4_dopant_val, a5_dopant_val]
                                                        profile_type = ['Linear', 'Constant', 'Constant', 'Constant',
                                                                        'Constant']
                                                        materials = ['GeO2-SiO2', 'F-SiO2_2', 'GeO2-SiO2',
                                                                     'SiO2', 'SiO2']
                                                        alphas = [a1_alpha_val, alpha_a2, alpha_a3, alpha_a4, alpha_a5]

                                                        # if working with one number of steps
                                                        if i == 0:
                                                            fiber_profile.delete_layers()
                                                            # build profile
                                                            fiber_profile.builder_profile(dev, sizes, dop_perct, profile_type,
                                                                                          materials, alphas, n_steps_val)
                                                        else:
                                                            fiber_profile.update_profile(dev, sizes, dop_perct, profile_type,
                                                                                         materials, alphas, n_steps_val)

                                                        '''#for studying different the number of steps
                                                        fiber_profile.delete_layers()
                                                        # build profile
                                                        fiber_profile.builder_profile(dev, sizes, dop_perct, profile_type,
                                                                                          materials, alphas, n_steps_val)'''
                                                        fiber_profile.set_wavelength(dev, wavelength_steps_val)


                                                        # running simulation
                                                        data_mode1 = experiment.simulate(param_Scan, mode='1')
                                                        # running simulation mode 2
                                                        data_mode2 = experiment.simulate(param_Scan, mode='3')
                                                        # running simulation mode 3
                                                        # data_mode3 = experiment.simulate(param_Scan, mode='5')

                                                        data = np.hstack((data_mode1, data_mode2))

                                                        data_scan[i, p:] = list(data)
                                                        data_scan[i, 0:p] = [a1_val, a2_val, a3_val, a4_val,
                                                                             a5_val, a1_dopant_val,
                                                                             a2_dopant_val, a3_dopant_val,
                                                                             a4_dopant_val, a5_dopant_val,
                                                                             a1_alpha_val, wavelength_steps_val,
                                                                             n_steps_val]
                                                        # Record the end time
                                                        end_time = time.time()
                                                        # Calculate the elapsed time
                                                        elapsed_time[i] = np.round(end_time - start_time, 2)
                                                        print("Simulation goes for: " + str(
                                                            100 * i / steps) + ' %' + f" It took: {elapsed_time[i]} seconds")
                                                        i = i + 1

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
    print(f'The average simulation time was: {np.round(np.average(elapsed_time), 2)} seconds')
    elapsed_time_h = np.round(np.sum(elapsed_time) / 3600, 2)
    print(f'The total simulation time was: {elapsed_time_h} hours')
