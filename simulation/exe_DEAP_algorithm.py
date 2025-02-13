import random
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import time

from fiber.core_profile_index_builder import ProfileIndexBuilder
from fiber.core_type import FiberParameters
from simulation import SimulationRun
from simulation import core_DEAP_algorithm


from deap import base, creator, tools, algorithms
from pdPythonLib import *
from datetime import datetime
import mplcursors

start_time = time.time()

matplotlib.use('TkAgg')
# Get the current date and time
current_time = datetime.now()

# Convert the date and time to a string
time_string = current_time.strftime("%Y-%m-%d_%H-%M-%S")

results_file = 'pareto_front_three_layers_GeO2' + time_string + '.csv'  # MODIFY
# Open the CSV file in written mode
f = open(results_file, 'w')

# FIMMWAVE
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
param = core_type.core_type_meth('three layers all GeO2 dp')

# Unpack attributes directly
sizes, dop_perct, profile_type, materials, alphas, n_steps, dev = (
    param.sizes, param.dop_perct, param.profile_type,
    param.materials, param.alphas, param.n_steps, param.dev
)

fiber_profile.delete_layers()
fiber_profile.builder_profile(dev, sizes, dop_perct, profile_type, materials, alphas, n_steps)

# Define the constraints for each parameter
a1 = [(3, 5)]
a2 = [(2, 5)]
a3 = [(2, 5)]
a4 = [(30, 30)]

dop_a1 = [(0, 0.1)]
dop_a2 = [(0, 0.1)]
dop_a3 = [(0, 0.1)]
dop_a4 = [(0, 0)]

alpha_a1 = [(0, 0)]
alpha_a2 = [(0, 0)]
alpha_a3 = [(0, 0)]
alpha_a4 = [(0, 0)]

constraints = a1 + a2 + a3 + dop_a1 + dop_a2 + dop_a3
# Set initial parameter values with random values within constraints
initial_values = [
    random.uniform(min_value, max_value) for min_value, max_value in constraints
]
# Configure the progress bar, it depends on the:
# initial population(n),
n = 20
# number of individuals selected for the next generation
mu = 10
# offspring from the population (lambda_) and
lambda_ = 15
# number of generations (ngen)
ngen = 10

# simulation
experiment = SimulationRun(fimmap)
experiment.solver_config('FDM Fiber Solver')
try:
    # execute the DEAP algorithm
    optimization = core_DEAP_algorithm(fimmap, fiber_profile, experiment)
    optm_population = optimization.algorithm_execution(n, mu, lambda_, ngen, initial_values, constraints)

except Exception as e:
    # Handle the exception
    print(f'An error occurred in the for iteration: {str(e)}')
finally:
    # The Pareto front solutions are now in the 'optm_population' variable
    # Extracting a1 values and objective values from the Pareto front
    a1_values = [ind[0] for ind in optm_population]
    obj1_values = [ind.fitness.values[0] for ind in optm_population]
    obj2_values = [ind.fitness.values[1] for ind in optm_population]
    obj3_values = [ind.fitness.values[2] for ind in optm_population]

    # Write the header row
    header = (['a1', 'a2', 'a3', 'dop_a1', 'dop_a2', 'dop_a3', 'disp', 'slope', 'dD/dF'])
    # variable to store the data
    data = np.zeros((len(obj1_values), len(header)))
    i = 0
    # Write the data for each individual in the Pareto front into data variable
    for ind in optm_population:
        a1_val, a2_val, a3_val, dop_a1_val, dop_a2_val, dop_a3_val = ind[0], ind[1], ind[2], ind[3], ind[4], ind[5]
        obj1_val, obj2_val, obj3_val = ind.fitness.values[0], ind.fitness.values[1], ind.fitness.values[2]
        data[i, :] = [a1_val, a2_val, a3_val, dop_a1_val, dop_a2_val, dop_a3_val, obj1_val, obj2_val, obj3_val]
        i = i + 1

    data_scan = data.astype('float')
    # add the new row to the top of the array
    data_scan = np.vstack((header, data_scan))

    for element in data_scan:
        f.write(','.join(element) + '\n')
    f.close()

    # Find the solution with the minimum obj1_val and obj2_val above X
    min_obj1_val = float('inf')  # Initialize to positive infinity
    best_solution = None
    # minimum
    thr = 0.07
    thr_dD_fab = 0.4
    for ind in optm_population:
        obj1_val, obj2_val, obj3_val = ind.fitness.values[0], ind.fitness.values[1], ind.fitness.values[2]
        if obj1_val < min_obj1_val and obj2_val < thr and obj3_val < thr_dD_fab:
            min_obj1_val = obj1_val
            best_solution = ind

    if best_solution:
        print("Best solution with the minimum dispersion and slope bellow 0.08:")
        print("a1:", best_solution[0])
        print("a2:", best_solution[1])
        print("a2:", best_solution[2])
        print("a1_dopa:", best_solution[3])
        print("a2_dopa:", best_solution[4])
        print("a3_dopa:", best_solution[5])
        print("Dispersion:", best_solution.fitness.values[0])
        print("Slope:", best_solution.fitness.values[1])
        print("dD/dF_0.1um:", best_solution.fitness.values[2])
    else:
        print("No solution found with obj2_val below X")

    # setting FIMMWAVE at the best solution
    sizes[0] = best_solution[0]
    sizes[1] = best_solution[1]
    sizes[2] = best_solution[2]
    dop_perct[0] = best_solution[3]
    dop_perct[1] = best_solution[4]
    dop_perct[2] = best_solution[5]
    fiber_profile.update_profile(dev, sizes, dop_perct, profile_type, materials, alphas, n_steps)
    wavelength = 1.55
    fiber_profile.set_wavelength(dev, wavelength)

    # Record the end time
    end_time = time.time()
    t = np.round(end_time - start_time, 3) / 60
    print(f'The simulation took: {t} minutes')

    # Plotting the Pareto front in 3D
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Plotting the Pareto front with obj3_values on the z-axis
    scatter = ax.scatter(obj1_values, obj2_values, obj3_values, marker='o', color='b', label='Pareto Front')

    ax.set_xlabel('Dispersion')
    ax.set_ylabel('Slope')
    ax.set_zlabel('dD/dF_0.1um')
    ax.set_title('Pareto Front')

    # Add a legend
    ax.legend()

    # Add interactivity with mplcursors
    mplcursors.cursor(hover=True)

    # Show the plot interactively
    plt.show()
