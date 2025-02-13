'''
This file has the objetive of taking of finding the best value based on required parameter using
Particle Swamp Optimization (PSO) algorithm
'''

import time
import numpy as np
from pdPythonLib import *
from datetime import datetime
from simulation_run import *
from core_profile_index_builder import *
from time_wind_simulation import *
from core_type import FiberParameters

PARAMETERS_SCAN: dict[str, bool] = {"beta": True, "neff": True, "a_eff": True, "alpha": True, "dispersion": True,
                                    "isLeaky": True,
                                    "neffg": True, "fillFac": True, "gammaE": True}
MAX_DISPERSION_PENALIZATION = 50


# Define the objective function
def objective_function(parameters):
    """
    Calculate the dispersion value for a given set of fiber parameters.

    Parameters:
    - parameters (tuple): A tuple containing the values of fiber parameters,
      where parameters[n] corresponds to an n parameter of the fiber core, depending on the core type.

    Returns:
    - float: The dispersion value calculated based on the provided fiber parameters.

    This function updates the fiber profile with the given parameters, runs simulations
    for mode 1 and mode 3 using FIMMWAVE, and retrieves the dispersion value. If the
    obtained dispersion value is outside the desired range (MIN_DISPERSION_LIMIT to MAX_DISPERSION_LIMIT),
    it is penalized using an exponential penalty function.
    If the simulation for mode 2 indicates isleakyMode2 as 2 (mode guided), the dispersion is set to MAX_DISPERSION_LIMIT.
    """

    # Initial parameters, defining the core type
    core_type = FiberParameters()

    # Getting the standard constructive parameters for the study core profile
    param = core_type.core_type_meth("step index with trench F-SiO2_1")

    # Unpack attributes directly from the core type method
    sizes, dop_perct, profile_type, materials, alphas, n_steps, dev = (
        param.sizes, param.dop_perct, param.profile_type,
        param.materials, param.alphas, param.n_steps, param.dev
    )

    # Unpack the variables
    a1, a2, a3, dop_a1 = parameters

    # Replace the variable parameters
    sizes[0] = a1
    sizes[1] = a1
    sizes[2] = a1
    dop_perct[0] = dop_a1

    # Update the core profile with the new characteristics
    fiber_profile.update_profile(dev, sizes, dop_perct, profile_type,
                                 materials, alphas, n_steps)

    # Running simulation
    # get the data for the 1rst and 2nd LP modes;
    # since we configure both polarizations, the 2nd mode corresponds to '3'
    data_mode1 = experiment.simulate(PARAMETERS_SCAN, mode='1')
    data_mode3 = experiment.simulate(PARAMETERS_SCAN, mode='3')

    # get the dispersion value for mode 1 and the guided status of mode 1 nad 2
    dispersion_mode1 = data_mode1[4]
    is_leaky_mode1 = data_mode1[5]
    is_leaky_mode2 = data_mode3[5]

    # Penalization
    if is_leaky_mode1 == 1 or is_leaky_mode2 == 2:
        dispersion_mode1 = MAX_DISPERSION_PENALIZATION

    print('disp: ', dispersion_mode1)

    return dispersion_mode1


# Define the PSO algorithm
def pso(objective_func, bounds, num_particles, max_iterations):
    # Creating variable to save the algorithm data
    header = (['a1', 'a2', 'a3', 'dop_a1', 'iteration', 'best global result'])
    data = np.zeros((max_iterations, len(header)))

    # Initialize the particles' positions and velocities
    particles = np.random.uniform(low=np.array(bounds)[:, 0], high=np.array(bounds)[:, 1],
                                  size=(num_particles, len(bounds)))
    velocities = np.zeros_like(particles)

    # Initialize the personal best positions and values
    personal_best_positions = particles.copy()
    personal_best_values = np.array([objective_func(p) for p in particles])

    # Initialize the global best position and value
    global_best_index = np.argmin(personal_best_values)
    global_best_position = personal_best_positions[global_best_index]
    global_best_value = personal_best_values[global_best_index]

    # Iterate through the specified number of iterations
    for i in range(max_iterations):
        print('***************The simulation goes %d%% *****************' % ((i / max_iterations) * 100))
        # Update the velocities and positions of the particles
        r1 = np.random.random(size=(num_particles, len(bounds)))
        r2 = np.random.random(size=(num_particles, len(bounds)))

        velocities = velocities + 2.5 * r1 * (personal_best_positions - particles) + 0.8 * r2 * (
                global_best_position - particles)
        particles = particles + velocities

        # Apply boundary constraints
        particles = np.clip(particles, np.array(bounds)[:, 0], np.array(bounds)[:, 1])
        particles = np.round(particles,4)

        # Evaluate the objective function for the new positions
        values = np.array([objective_func(p) for p in particles])

        # Update personal best positions and values
        mask = values < personal_best_values
        personal_best_positions[mask] = particles[mask]
        personal_best_values[mask] = values[mask]

        # Replace the personal best positions with 50 for values less than zero
        mask_negative_values = personal_best_values < 0
        personal_best_values[mask_negative_values] = 50

        # Update global best position and value
        best_index = np.argmin(personal_best_values)
        if personal_best_values[best_index] < global_best_value:
            global_best_position = personal_best_positions[best_index]
            global_best_value = personal_best_values[best_index]
        # Eliminating rare values

        # Saving data
        data[i, :] = [global_best_position[0], global_best_position[1], global_best_position[2], global_best_position[3], i, global_best_value]

    # Writing data into csv file
    data_scan = data.astype('float')
    # add the new row to the top of the array
    data_scan = np.vstack((header, data_scan))

    return global_best_position, data_scan



# Get the current date and time
current_time = datetime.now()

# Convert the date and time to a string
time_string = current_time.strftime("%Y-%m-%d_%H-%M-%S")

results_file = 'PSO_' + 'step_index_with_trench_F-SiO2_1' + time_string + '.csv'  # MODIFY
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

# build profile
# Initial parameters
core_type = FiberParameters()
param = core_type.core_type_meth("step index with trench F-SiO2_1")

# Unpack attributes directly
sizes, dop_perct, profile_type, materials, alphas, n_steps, dev = (
    param.sizes, param.dop_perct, param.profile_type,
    param.materials, param.alphas, param.n_steps, param.dev
)

fiber_profile.delete_layers()
fiber_profile.builder_profile(dev, sizes, dop_perct, profile_type, materials, alphas, n_steps)

# RUN THE OPTIMIZATION
## variation of input parameters MODIFY
# Defines the ranges for each parameter (constrains)
a1 = [(3, 6)]
a2 = [(2, 4)]
a3 = [(2, 6)]
a4 = [(30, 30)]

dop_a1 = [(0, 0.1)]
dop_a2 = [(0, 0)]
dop_a3 = [(0, 0)]
dop_a4 = [(0, 0)]

alpha_a1 = [(0, 0)]
alpha_a2 = [(0, 0)]
alpha_a3 = [(0, 0)]
alpha_a4 = [(0, 0)]

# Define the bounds for each variable (constrains)
constraints = a1 + a2 + a3 + dop_a1

# simulation
experiment = SimulationRun(fimmap)
experiment.solver_config('GFS Fiber Solver')

# Set the parameters for the PSO algorithm
num_particles = 50
max_iterations = 100

try:
    # Run the PSO algorithm
    best_solution, data_scan = pso(objective_function, constraints, num_particles, max_iterations)

except Exception as e:
    # Handle the exception
    print(f'An error occurred in the for loop: {str(e)}')
finally:
    for element in data_scan:
        f.write(','.join(element) + '\n')
    f.close()

    # Extract the best values for each variable
    best_a1,  best_a2, best_a3, best_dop1 = best_solution

    # Print the best combination and the corresponding minimum value
    print("Best Combination:")
    print("a1:", best_a1)
    print("a2:", best_a2)
    print("a3:", best_a3)
    #print("a4:", best_a4)
    print("dop1:", best_dop1)
    #print("dop2:", best_dop2)
    #print("dop3:", best_dop3)
    #print("dop4:", best_dop4)
    #print("alpha_a1:", best_alpha_a1)
    #print("alpha_a2:", best_alpha_a2)
    #print("alpha_a3:", best_alpha_a3)
    #print("alpha_a4:", best_alpha_a4)

    min_disp = objective_function(best_solution)
    print("Minimum Disp:", min_disp)

    # load the best result into FIMMWAVE
    # Unpack attributes directly from the core type method
    sizes, dop_perct, profile_type, materials, alphas, n_steps, dev = (
        param.sizes, param.dop_perct, param.profile_type,
        param.materials, param.alphas, param.n_steps, param.dev
    )

    # Replace the variable parameters
    sizes[0] = best_a1
    sizes[1] = best_a2
    sizes[2] = best_a3
    dop_perct[0] = best_dop1

    # Update the core profile with the new characteristics
    fiber_profile.update_profile(dev, sizes, dop_perct, profile_type,
                                 materials, alphas, n_steps)

