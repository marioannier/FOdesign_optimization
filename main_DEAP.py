import random
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import time

from deap import base, creator, tools, algorithms
from pdPythonLib import *
from datetime import datetime
from simulation_run import *
from core_profile_index_builder import *
from collections.abc import Sequence
from itertools import repeat
from core_type import FiberParameters
import mplcursors
from deap.tools import Statistics

from typing import Tuple

# Define the reasonable limit before penalizing
MIN_DISPERSION_LIMIT = 0
MAX_DISPERSION_PENALIZATION = 50
MIN_SLOPE_AVERAGE = 0
WORKING_WAVELENGTH = 1.55
COUNTER = 0

PARAMETERS_SCAN: dict[str, bool] = {"beta": True, "neff": True, "a_eff": True, "alpha": True, "dispersion": True,
                                    "isLeaky": True,
                                    "neffg": True, "fillFac": True, "gammaE": True}


def exponential_penalty_function(x, x_optimal, alpha=0.1, lambda_param=0.5):
    """
    Compute the Exponential Penalty Function.

    Parameters:
    - x: Current solution vector.
    - x_optimal: Optimal solution vector.
    - alpha: Exponential rate parameter.
    - lambda_param: Penalty strength parameter.

    Returns:
    - penalty: Penalty value based on the exponential penalty function.
    """
    # Calculate the Euclidean norm (distance) between the current solution and the optimal solution
    deviation = np.linalg.norm(x - x_optimal)

    # Compute the penalty using the exponential penalty function formula
    penalty = lambda_param * np.exp(alpha * deviation)
    return penalty


def feasible(individual):
    """
    Feasibility function for the individual. Returns True if feasible, False otherwise.

    Parameters:
    - individual (list): The individual to be checked for feasibility.
    - constraints (list of tuples): List of tuples defining the constraints for each attribute.

    Returns:
    - bool: True if the individual is feasible, False otherwise.
    """
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

    for i, (min_value, max_value) in enumerate(constraints):
        if not (min_value <= individual[i] <= max_value):
            return False
    return True


def distance(individual):
    """
    A quadratic distance function to the feasibility region, enhancing the attraction of the bowl.

    Parameters:
    - individual (list): The individual for which to calculate the distance.
    - constraints (list of tuples): List of tuples defining the constraints for each attribute.

    Returns:
    - float: The quadratic distance from the feasibility region.

    This function calculates the quadratic distance from the feasibility region based on the constraints
    for each attribute. It enhances the attraction of the bowl-shaped feasible region by using the quadratic
    distance function h(x) = Δ + (x - x0)^2, where x0 is the approximate edge of the valid zone.
    """

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

    total_distance = 0.0

    for i, (min_value, max_value) in enumerate(constraints):
        if individual[i] < min_value:
            total_distance += (min_value - individual[i]) ** 2
        elif individual[i] > max_value:
            total_distance += (individual[i] - max_value) ** 2

    return total_distance


def objective_function_dispersion(parameters):
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
    param = core_type.core_type_meth('three layers all GeO2 dp')

    # Unpack attributes directly from the core type method
    sizes, dop_perct, profile_type, materials, alphas, n_steps, dev = (
        param.sizes, param.dop_perct, param.profile_type,
        param.materials, param.alphas, param.n_steps, param.dev
    )

    # Unpack the variables
    a1, a2, a3, dop_a1, dop_a2, dop_a3 = parameters

    # Replace the variable parameters
    sizes[0] = a1
    sizes[1] = a2
    sizes[2] = a3
    dop_perct[0] = dop_a1
    dop_perct[1] = dop_a2
    dop_perct[2] = dop_a3

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

    # dispersion_mode1 = np.abs(dispersion_mode1 - MIN_DISPERSION_LIMIT)

    # Penalization
    if is_leaky_mode1 == 1 or is_leaky_mode2 == 2:
        dispersion_mode1 = MAX_DISPERSION_PENALIZATION
    if dispersion_mode1 < 0:
        dispersion_mode1 = MAX_DISPERSION_PENALIZATION

    return dispersion_mode1


def objective_function_slope(parameters):
    """
    Calculate the absolute average slope of dispersion with respect to wavelength
    for a given set of fiber parameters.

    Parameters:
    - parameters (tuple): A tuple containing the values of fiber parameters,
      where parameters[n] corresponds to an n parameter of the fiber core, depending on the core type.

    Returns:
    - float: The absolute average slope of dispersion with respect to wavelength
             calculated based on the provided fiber parameters.
    """
    # Initial parameters, defining the core type
    core_type = FiberParameters()

    # Getting the standard constructive parameters for the study core profile
    param = core_type.core_type_meth('three layers all GeO2 dp')

    # Unpack attributes directly from the core type method
    sizes, dop_perct, profile_type, materials, alphas, n_steps, dev = (
        param.sizes, param.dop_perct, param.profile_type,
        param.materials, param.alphas, param.n_steps, param.dev
    )

    # Unpack the variables
    a1, a2, a3, dop_a1, dop_a2, dop_a3 = parameters

    # Replace the variable parameters
    sizes[0] = a1
    sizes[1] = a2
    sizes[2] = a3
    dop_perct[0] = dop_a1
    dop_perct[1] = dop_a2
    dop_perct[2] = dop_a3

    # Update the core profile with the new characteristics
    fiber_profile.update_profile(dev, sizes, dop_perct, profile_type,
                                 materials, alphas, n_steps)

    # Define wavelength range and the sampling interval (lam_e-lam_s)/number_steps
    number_steps = 7
    lam_s = 1.53
    lam_e = 1.56
    steps = np.linspace(lam_s, lam_e, number_steps)

    # Running simulation
    # get the data for the 1rst mode;
    data_mode1 = np.zeros((number_steps, 9))

    # Iterate over all scaling values
    for i, wavelength in enumerate(steps):
        # setting the work wavelength
        fiber_profile.set_wavelength(dev, wavelength)
        # running simulation
        data_mode1[i, :] = experiment.simulate(PARAMETERS_SCAN, mode='1')

    # setting to 1.55 at the end of the analysis
    fiber_profile.set_wavelength(dev, WORKING_WAVELENGTH)

    # Calculate the derivative of dispersion with respect to wavelength
    slope = np.diff(data_mode1[:, 4]) / np.diff(steps * 1000)  # transform the wavelength to nm

    # Calculate the average slope
    slope_ave = np.average(slope)
    output = np.abs(slope_ave)

    # bound the objetive function
    if output > 0.5 or output == 0:
        output = 60

    return output


def objective_function_err_fab(parameters):
    """
    Calculate the average absolute derivative of dispersion with respect to wavelength
    for different scaling factors, simulating fabrication errors for a given set of fiber parameters.

    Parameters:
    - parameters (tuple): A tuple containing the values of fiber parameters,
      where parameters[n] corresponds to an n parameter of the fiber core, depending on the core type.

    Returns:
    - float: The average absolute derivative of dispersion with respect to wavelength
             calculated based on the provided fiber parameters and simulated fabrication errors.
    """

    # Define constants
    ERR_FAB_MAX = 0.1
    SCALING_STEPS = 3

    # Initial parameters, defining the core type
    core_type = FiberParameters()

    # Getting the standard constructive parameters for the study core profile
    param = core_type.core_type_meth('three layers all GeO2 dp')

    # Unpack attributes directly from the core type method
    sizes, dop_perct, profile_type, materials, alphas, n_steps, dev = (
        param.sizes, param.dop_perct, param.profile_type,
        param.materials, param.alphas, param.n_steps, param.dev
    )

    # Unpack the variables
    a1, a2, a3, dop_a1, dop_a2, dop_a3 = parameters

    # Replace the variable parameters
    sizes[0] = a1
    sizes[1] = a2
    sizes[2] = a3
    dop_perct[0] = dop_a1
    dop_perct[1] = dop_a2
    dop_perct[2] = dop_a3

    # scaling variable, first I find the ratio between the ERR_FAB_MAX and the central core diameter
    # this is translated to a scaling factor. I.e. how much the scaling factor needs to change in order
    # to introduce an error in fabrication of ERR_FAB_MAX
    rep_factor_scala = ERR_FAB_MAX / a1
    # Then I find the scaling factor values
    steps = np.linspace(1 - rep_factor_scala, 1 + rep_factor_scala, SCALING_STEPS)
    data_mode1 = np.zeros((SCALING_STEPS, 9))

    # determine the dispersion for each factor of scale from -ERR_FAB_MAX to ERR_FAB_MAX
    for i, sca_fact in enumerate(steps):
        sizes[0] = a1 * sca_fact
        sizes[1] = a2 * sca_fact
        sizes[2] = a3 * sca_fact
        fiber_profile.update_profile(dev, sizes, dop_perct, profile_type, materials, alphas, n_steps)
        # running simulation
        data_mode1[i, :] = experiment.simulate(PARAMETERS_SCAN, mode='1')

    # Calculate the derivative of dispersion with respect to an ERR_FAB_MAX
    scaling_intervals = 2 * ERR_FAB_MAX / (SCALING_STEPS - 1)
    fac = ERR_FAB_MAX / scaling_intervals
    diff_err_fab = fac * np.diff(data_mode1[:, 4])

    # determining the absolute value
    output = np.abs(np.average(diff_err_fab))

    # bound the objetive function
    if output > 0.5 or output == 0:
        output = 60

    return output


def evaluate(individual):
    """
    Evaluate an individual using multiple objective functions.

    Parameters:
    - individual (tuple): A tuple containing the values of fiber parameters,
      where individual[n] corresponds to an n parameter of the fiber core, depending on the core type.

    Returns:
    - tuple: A tuple containing the values of multiple objective functions calculated based on the individual's parameters.
    """
    # Call the objective_function with the individual's parameters
    # Objective 1 calculation
    disp = objective_function_dispersion(individual)
    obj1 = disp

    # Objective 2 calculation
    slope = objective_function_slope(individual)
    obj2 = slope

    # Objective 3 calculation
    dif_fab_err = objective_function_err_fab(individual)
    obj3 = dif_fab_err

    return obj1, obj2, obj3


# Function to initialize individuals
def initIndividual(icls, content, ccls, constraints):
    # create n individuals with ramdom values into the constraint limits
    part = icls(content)
    for i, (min_value, max_value) in enumerate(constraints):
        part[i] = random.uniform(min_value, max_value)
    return part


def custom_mutGaussian_constraints(individual, mu, sigma, indpb, constraints):
    """This function applies a gaussian mutation on the input individual
    while keeping the mutated values within the specified constraints.

    :param individual: Individual to be mutated.
    :param mu: Mean or :term:`python:sequence` of means for the
               gaussian addition mutation.
    :param sigma: Standard deviation or :term:`python:sequence` of
                  standard deviations for the gaussian addition mutation.
    :param indpb: Independent probability for each attribute to be mutated.
    :param constraints: List of tuples defining the constraints for each attribute.
    :returns: A tuple of one individual.

    This function uses the :func:`~random.random` and :func:`~random.gauss`
    functions from the Python base :mod:`random` module.
    """
    size = len(individual)
    if not isinstance(mu, Sequence):
        mu = repeat(mu, size)
    elif len(mu) < size:
        raise IndexError("mu must be at least the size of individual: %d < %d" % (len(mu), size))
    if not isinstance(sigma, Sequence):
        sigma = repeat(sigma, size)
    elif len(sigma) < size:
        raise IndexError("sigma must be at least the size of individual: %d < %d" % (len(sigma), size))

    for i, m, s, (min_value, max_value) in zip(range(size), mu, sigma, constraints):
        if random.random() < indpb:
            mutated_value = individual[i] + random.gauss(m, s)
            individual[i] = max(min(mutated_value, max_value), min_value)
        else:
            individual[i] = max(min(individual[i], max_value), min_value)
    return individual


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

# simulation
experiment = SimulationRun(fimmap)
experiment.solver_config('FDM Fiber Solver')

# Define the optimization problem
creator.create("FitnessMulti", base.Fitness, weights=(-1.0, -1.0, -1.0))
creator.create("Individual", list, fitness=creator.FitnessMulti)

# Configure the optimization problem
toolbox = base.Toolbox()
toolbox.register("individual", initIndividual, creator.Individual, initial_values, list, constraints)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", evaluate)
toolbox.decorate("evaluate", tools.DeltaPenalty(feasible, (30, 3, 3), distance))
toolbox.register("mate", tools.cxBlend, alpha=0.5)
toolbox.register("mutate", custom_mutGaussian_constraints, mu=0, sigma=0.8, indpb=0.5, constraints=constraints)
toolbox.register("select", tools.selNSGA2)

# Configure the progress bar, it depends on the:
# initial population(n),
n = 200
# number of individuals selected for the next generation
mu = 100
# offspring from the population (lambda_) and
lambda_ = 150
# number of generations (ngen)
ngen = 100

''''# total iterations (working on)
global global_total
global_total = n + lambda_ * ngen
global global_counter
global_counter = 0'''

# Create the initial population
population = toolbox.population(n)

# Create a Statistics object and register the desired statistics
stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("min", np.min, axis=0)
stats.register("max", np.max, axis=0)
stats.register("avg", np.mean, axis=0)
stats.register("std", np.std, axis=0)

logbook = tools.Logbook()

# Evaluate the individuals with an invalid fitness
'''invalid_ind = [ind for ind in population if not ind.fitness.valid]
fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
for ind, fit in zip(invalid_ind, fitnesses):
    ind.fitness.values = fit'''

try:
    # Run the optimization algorithm with stats
    _, logbook = algorithms.eaMuPlusLambda(population, toolbox, mu=mu, lambda_=lambda_, cxpb=0.5, mutpb=0.5,
                                           ngen=ngen,
                                           stats=stats,
                                           halloffame=None, verbose=True)

except Exception as e:
    # Handle the exception
    print(f'An error occurred in the for loop: {str(e)}')
finally:
    # The Pareto front solutions are now in the 'population' variable
    # Extracting a1 values and objective values from the Pareto front
    a1_values = [ind[0] for ind in population]
    obj1_values = [ind.fitness.values[0] for ind in population]
    obj2_values = [ind.fitness.values[1] for ind in population]
    obj3_values = [ind.fitness.values[2] for ind in population]

    # Write the header row
    header = (['a1', 'a2', 'a3', 'dop_a1', 'dop_a2', 'dop_a3', 'disp', 'slope', 'dD/dF'])
    # variable to store the data
    data = np.zeros((len(obj1_values), len(header)))
    i = 0
    # Write the data for each individual in the Pareto front into data variable
    for ind in population:
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
    for ind in population:
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
