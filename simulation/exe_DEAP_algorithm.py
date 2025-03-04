import random
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import time
import mplcursors

from fiber.core_profile_index_builder import ProfileIndexBuilder
from fiber.core_type import FiberParameters
from simulation import SimulationRun
from simulation import core_DEAP_algorithm

from pdPythonLib import *
from datetime import datetime

start_time = time.time()
matplotlib.use('TkAgg')

# Get the current date and time
current_time = datetime.now()

# Convert the date and time to a string
time_string = current_time.strftime("%Y-%m-%d_%H-%M-%S")

# build profile with index-profile:
type_index_profile = 'W shape F-SiO2_2 with ring'
results_file = type_index_profile + time_string + '.csv'

# Open the CSV file in written mode
f = open(results_file, 'w')

# FIMMWAVE
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

dev = "app.subnodes[1].subnodes[1]"

# Initial parameters
core_type = FiberParameters()

param = core_type.core_type_meth(type_index_profile)

# Unpack attributes directly
sizes, dop_perct, profile_type, materials, alphas, n_steps, dev = (
    param.sizes, param.dop_perct, param.profile_type,
    param.materials, param.alphas, param.n_steps, param.dev
)

fiber_profile.delete_layers()
fiber_profile.builder_profile(dev, sizes, dop_perct, profile_type, materials, alphas, n_steps)

# Define the constraints for each parameter
a1 = [(1.5, 5)]
a2 = [(1.5, 5)]
a3 = [(1.5, 5)]
a4 = [(50, 50)]

dop_a1 = [(0.005, 0.1)]
dop_a2 = [(0, 0)]
dop_a3 = [(0, 0.1)]  # Original constraint (will be overridden)
dop_a4 = [(0, 0)]

alpha_a1 = [(0, 0)]
alpha_a2 = [(0, 0)]
alpha_a3 = [(0, 0)]
alpha_a4 = [(0, 0)]

constraints = a1 + a2 + a3 + dop_a1 + dop_a2 + dop_a3

# Generate initial values with dop_a3 ∈ [0, dop_a1]
initial_values = []
for i, (orig_min, orig_max) in enumerate(constraints):
    if i == 5:  # dop_a3 is the 6th parameter (index 5)
        # Get already-generated dop_a1 value (index 3)
        current_max = initial_values[3]
        val = round(random.uniform(0, current_max), 3)  # Force min=0
    elif orig_min == orig_max:  # Fixed parameters (a4, zeros, etc.)
        val = orig_min
    else:
        val = round(random.uniform(orig_min, orig_max), 3)
    initial_values.append(val)

print(f'The initial values are {initial_values}')

# Configure the progress bar, it depends on:

# initial population(n),
n = 10
# number of individuals selected for the next generation
mu = 10
# offspring from the population (lambda_) and
lambda_ = 10
# number of generations (ngen)
ngen = 50

mean_d = 0

# Define percentage of range to use as sigma (e.g., 10%)
# Small (s=0.01)	Tiny changes, slow but precise optimization.
# Medium (s=0.1)	Balanced exploration and refinement.
# Large (s=1.0)	Big jumps, high exploration but risk of instability.
sigma_fraction = 0.1
# Compute sigma values and round to 4 decimal places
sigma = [
    round(sigma_fraction * (max_val - min_val), 4) if max_val > min_val else 0
    for min_val, max_val in constraints
]

''' 
BIAS MUTTATION->NOT RECOMENDED
mean_fraction = 0.05    # e.g., 5% of the range for mu
# Compute mu values and round to 4 decimal places
mean_d = [
    round(mean_fraction * (max_val - min_val), 4) if max_val > min_val else 0
    for min_val, max_val in constraints
]
'''
# UNBIAS MUTTATION->RECOMENDED
mean_d = 0

indpb = 0.5

# simulation
experiment = SimulationRun(fimmap)
experiment.solver_config('GFS Fiber Solver')
try:
    # execute the DEAP algorithm
    optimization = core_DEAP_algorithm.CoreDEAPAlgorithm(fimmap, fiber_profile, experiment, type_index_profile)
    optm_population = optimization.algorithm_execution(n, mu, lambda_, ngen, initial_values, mean_d, sigma, indpb,
                                                       constraints)

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
    best_solution = None
    # minimum
    thr_D = 0
    thr_Slope = 0.5
    thr_dD_fab = 0.4
    for ind in optm_population:
        obj1_val, obj2_val, obj3_val = ind.fitness.values[0], ind.fitness.values[1], ind.fitness.values[2]
        if obj1_val < float('inf') and obj2_val < float('inf') and obj3_val < float('inf'):
            min_obj1_val = obj1_val
            best_solution = ind

    if best_solution:
        print("Best solution with the minimum dispersion and slope bellow 0.08:")
        print("a1:", best_solution[0])
        print("a2:", best_solution[1])
        print("a3:", best_solution[2])
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
