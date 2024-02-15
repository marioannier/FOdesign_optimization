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


# Define the objective function
def objective_function(parameters):
    # Unpack the variables
    # initial parameters
    a1, a2, a3, a4, dop_a1, dop_a2, dop_a3, dop_a4, alpha_a1, alpha_a2, alpha_a3, alpha_a4 = parameters

    # for now, only changing the sizes and dopant in PSO
    sizes = [a1, a2, a3, a4]
    dop_perct = [dop_a1, dop_a2, dop_a3, dop_a4]
    profile_type = ['Constant', 'Constant', 'Constant', 'Constant']
    materials = ['GeO2-SiO2', 'GeO2-SiO2','F-SiO2_1', 'SiO2']
    alphas = [alpha_a1, alpha_a1, alpha_a3, alpha_a4]
    n_steps = 2  # 2 for constant

    fiber_profile.update_profile(dev, sizes, dop_perct, profile_type,
                                 materials, alphas, n_steps)
    # running simulation
    param_Scan = {"beta": True, "neff": True, "a_eff": True, "alpha": True, "dispersion": True, "isLeaky": True,
                  "neffg": True, "fillFac": True, "gammaE": True}

    data_mode1 = experiment.simulate(param_Scan, mode='1')
    data_mode3 = experiment.simulate(param_Scan, mode='3')

    # get the dispersion
    disp = data_mode1[4]
    isleakyMode2 = data_mode3[5]
    # to avoid negative values, change later fot the finesse function
    if disp < 13.5:
        disp = 100
    if isleakyMode2 == 2:
        disp = 100

    print('The dispersion is: ', disp)

    return disp

# Define the PSO algorithm
def pso(objective_func, bounds, num_particles, max_iterations):
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
        print(i)
        # Update the velocities and positions of the particles
        r1 = np.random.random(size=(num_particles, len(bounds)))
        r2 = np.random.random(size=(num_particles, len(bounds)))

        velocities = velocities + 1.0 * r1 * (personal_best_positions - particles) + 2.0 * r2 * (
                global_best_position - particles)
        particles = particles + velocities

        # Apply boundary constraints
        particles = np.clip(particles, np.array(bounds)[:, 0], np.array(bounds)[:, 1])

        # Evaluate the objective function for the new positions
        values = np.array([objective_func(p) for p in particles])

        # Update personal best positions and values
        mask = values < personal_best_values
        personal_best_positions[mask] = particles[mask]
        personal_best_values[mask] = values[mask]

        # Update global best position and value
        best_index = np.argmin(personal_best_values)
        if personal_best_values[best_index] < global_best_value:
            global_best_position = personal_best_positions[best_index]
            global_best_value = personal_best_values[best_index]

    return global_best_position


# Get the current date and time
current_time = datetime.now()

# Convert the date and time to a string
time_string = current_time.strftime("%Y-%m-%d_%H-%M-%S")

results_file = 'PSO_'+'ProfileX_' + time_string + '.csv'  # MODIFY
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
# initial parameters
a1 = 3
a2 = 3
a3 = 3
a4 = 30

dop_a1 = 0.1
dop_a2 = 0
dop_a3 = 0
dop_a4 = 0

alpha_a1 = 0
alpha_a2 = 0
alpha_a3 = 0
alpha_a4 = 0

sizes = [a1, a2, a3, a4]
dop_perct = [dop_a1, dop_a2, dop_a3, dop_a4]
profile_type = ['Constant', 'Constant', 'Constant', 'Constant']
materials = ['GeO2-SiO2', 'GeO2-SiO2', 'F-SiO2_2', 'SiO2']
alphas = [alpha_a1, alpha_a1, alpha_a3, alpha_a4]
n_steps = 2  # 2 for constant
fiber_profile.delete_layers()
fiber_profile.builder_profile(dev, sizes, dop_perct, profile_type,
                              materials, alphas, n_steps)

# RUN THE OPTIMIZATION
## variation of input parameters MODIFY
# Defines the ranges for each parameter (constrains)
a1 = [(3, 5)]
a2 = [(2, 4)]
a3 = [(2, 4)]
a4 = [(30, 30)]

dop_a1 = [(0, 0.1)]
dop_a2 = [(0, 0.1)]
dop_a3 = [(0, 0)]
dop_a4 = [(0, 0)]

alpha_a1 = [(0, 0)]
alpha_a2 = [(0, 0)]
alpha_a3 = [(0, 0)]
alpha_a4 = [(0, 0)]

# Define the bounds for each variable (constrains)
bounds = a1 + a2 +a3 +a4 +dop_a1+dop_a2+dop_a3+dop_a4+alpha_a1+alpha_a2+alpha_a3+alpha_a4

# simulation
experiment = SimulationRun(fimmap)
experiment.solver_config('GFS Fiber Solver')

# Set the parameters for the PSO algorithm
num_particles = 30
max_iterations = 100

# Run the PSO algorithm
best_solution = pso(objective_function, bounds, num_particles, max_iterations)

# Extract the best values for each variable
best_a1, best_a2, best_a3, best_a4, best_dop1, best_dop2, best_dop3, best_dop4, best_alpha_a1, best_alpha_a2, best_alpha_a3, best_alpha_a4 = best_solution

# Print the best combination and the corresponding minimum value
print("Best Combination:")
print("a1:", best_a1)
print("a2:", best_a2)
print("a3:", best_a3)
print("a4:", best_a4)
print("dop1:", best_dop1)
print("dop2:", best_dop2)
print("dop3:", best_dop3)
print("dop4:", best_dop4)
print("alpha_a1:", best_alpha_a1)
print("alpha_a2:", best_alpha_a2)
print("alpha_a3:", best_alpha_a3)
print("alpha_a4:", best_alpha_a4)

min_disp = objective_function(best_solution)
print("Minimum Disp:", min_disp)
