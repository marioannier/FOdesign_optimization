import random
import matplotlib
from deap import base, creator, tools, algorithms
from datetime import datetime
import time
import numpy as np
from pdPythonLib import *
from datetime import datetime
from simulation_run import *
from core_profile_index_builder import *
from time_wind_simulation import *
import matplotlib.pyplot as plt
from deap import tools
from collections.abc import Sequence
from itertools import repeat
from core_type import FiberParameters
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import mplcursors

def objective_function_dispersion(parameters):
    # Initial parameters
    core_type = FiberParameters()
    param = core_type.core_type_meth('step index')

    # Unpack attributes directly
    sizes, dop_perct, profile_type, materials, alphas, n_steps, dev = (
        param.sizes, param.dop_perct, param.profile_type,
        param.materials, param.alphas, param.n_steps, param.dev
    )
    # Unpack the variables
    a1, dop_a1 = parameters
    # replacing variable parameters
    sizes[0] = a1
    dop_perct[0] = dop_a1

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
    if disp < 0 or disp > 30:
        disp = 100
    if isleakyMode2 == 2:
        disp = 100
    print("Dispersion: ", disp)
    return disp

def objective_function_slope(parameters):
    # Initial parameters
    core_type = FiberParameters()
    param = core_type.core_type_meth('step index')

    # Unpack attributes directly
    sizes, dop_perct, profile_type, materials, alphas, n_steps, dev = (
        param.sizes, param.dop_perct, param.profile_type,
        param.materials, param.alphas, param.n_steps, param.dev
    )
    # Unpack the variables
    a1, dop_a1 = parameters
    # replacing variable parameters
    sizes[0] = a1
    dop_perct[0] = dop_a1

    fiber_profile.update_profile(dev, sizes, dop_perct, profile_type,
                                 materials, alphas, n_steps)
    # these variables define the number of steps in terms of scaling factor
    number_steps = 7 # la razon de cambio es de 2 nm de cambio
    param_Name = ["lambda"]
    lam_s = 1.53
    lam_e = 1.56
    steps = np.linspace(lam_s, lam_e, number_steps)

    # running simulation
    param_Scan = {"beta": True, "neff": True, "a_eff": True, "alpha": True, "dispersion": True, "isLeaky": True,
                  "neffg": True, "fillFac": True, "gammaE": True}  # cambiar a falsos y reducir el tamaño de data_mode1

    data_mode1 = np.zeros((number_steps, 9))

    # Iterate over all scaling values
    for i, wavelength in enumerate(steps):
        # setting the work wavelength
        fiber_profile.set_wavelength(dev, wavelength)
        # running simulation
        data_mode1[i, :] = experiment.simulate(param_Scan, mode='1')

    #setting again to 1.55
    wavelength = 1.55
    fiber_profile.set_wavelength(dev, wavelength)

    # Calculate the derivative of dispersion with respect to wavelength
    slope = np.diff(data_mode1[:, 4]) / np.diff(steps * 1000)  # transform the wavelength to nm

    output = np.abs(np.average(slope))
    if output == 0:
        output = 10
    print("Slope: ", output)
    return output
def objective_function_err_fab(parameters):
    # Unpack the variables
    # initial parameters
    core_type = FiberParameters()
    param = core_type.core_type_meth('step index')

    # Unpack attributes directly
    sizes, dop_perct, profile_type, materials, alphas, n_steps, dev = (
        param.sizes, param.dop_perct, param.profile_type,
        param.materials, param.alphas, param.n_steps, param.dev
    )
    # Unpack the variables
    a1, dop_a1 = parameters
    # replacing variable parameters
    sizes[0] = a1
    dop_perct[0] = dop_a1

    # running simulation
    param_Scan = {"beta": True, "neff": True, "a_eff": True, "alpha": True, "dispersion": True, "isLeaky": True,
                  "neffg": True, "fillFac": True, "gammaE": True}

    # scaling variable (COMENTAR PARA ENTENDER)
    scaling_steps = 3
    err_max = 0.1
    rep_factor_scala = err_max/a1 #Traduccion de 0.3um de error a factor de escala pero solo para determinar la dispersion
    steps = np.linspace(1-rep_factor_scala, 1+rep_factor_scala, scaling_steps)
    data_mode1 = np.zeros((scaling_steps, 9))
    # aqui se determina la dispersion para cada fcator de escala desde -0.3um to 0.3um de error
    for i, sca_fact in enumerate(steps):
        sizes[0] = a1*sca_fact
        fiber_profile.update_profile(dev, sizes, dop_perct, profile_type, materials, alphas, n_steps)
        # running simulation
        data_mode1[i, :] = experiment.simulate(param_Scan, mode='1')

    # Calculate the derivative of dispersion with respect to wavelength
    scaling_intervals = 2*err_max/(scaling_steps-1)
    fac = 0.1/scaling_intervals# to convert to 0.1um
    diff_err_fab = fac * np.diff(data_mode1[:, 4])   # nm interval, i dont divide by 0.1 beacuse is include in the fac formula

    output = np.abs(np.average(diff_err_fab))
    if output == 0:
        output = 10
    print("dD/dF_0.1um: ", output)
    return output

def evaluate(individual):
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

    print('part: ', part)
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
    print('ind: ', individual)

    return individual


matplotlib.use('TkAgg')
# Get the current date and time
current_time = datetime.now()

# Convert the date and time to a string
time_string = current_time.strftime("%Y-%m-%d_%H-%M-%S")

results_file = 'pareto_front_results_' + time_string + '.csv'  # MODIFY
# Open the CSV file in written mode
f = open(results_file, 'w')

# FIMMWAVE
fimmap = pdApp()
fimmap.StartApp('C:\\Program Files\\PhotonD\\Fimmwave\\bin64\\fimmwave.exe', 5101)

# MODIFY DEPENDING ON PLACE OF WORKING
# from work
#test_dir = 'D:\\OneDrive UPV\\OneDrive - UPV\PhD-m\\2023-2024\\FiberDesin_PhotonD\\FOdesign_optimization'
# from personal computer
test_dir = 'C:\\Users\\Mario\\OneDrive - UPV\PhD-m\\2023-2024\\FiberDesin_PhotonD\\FOdesign_optimization'

fiber_profile = ProfileIndexBuilder(fimmap)
fiber_profile.create_fimm_project('test', test_dir)
fiber_profile.add_moduleFWG('Module 1')
fiber_profile.set_material_db(test_dir, '\\refbase_2.mat')
dev = "app.subnodes[1].subnodes[1]"

# build profile
# Initial parameters
core_type = FiberParameters()
param = core_type.core_type_meth('step index')

# Unpack attributes directly
sizes, dop_perct, profile_type, materials, alphas, n_steps, dev = (
    param.sizes, param.dop_perct, param.profile_type,
    param.materials, param.alphas, param.n_steps, param.dev
)

fiber_profile.delete_layers()
fiber_profile.builder_profile(dev, sizes, dop_perct, profile_type,materials, alphas, n_steps)

# Define the constraints for each parameter
constraints = [
    (3, 5),  # a1
    #(3, 5),  # a2
    #(3, 5),  # a3
    #(30, 30),  # a4
    (0.02, 0.12)  # dop_a1
    #(0, 0),  # dop_a2
    #(0, 0),  # dop_a3
    #(0, 0),  # dop_a4
    #(1, 1),  # alpha_a1
    #(0, 0),  # alpha_a2
    #(0, 0),  # alpha_a3
    #(0, 0),  # alpha_a4
]

# Set initial parameter values with random values within constraints
initial_values = [
    random.uniform(min_value, max_value) for min_value, max_value in constraints
]

# simulation
experiment = SimulationRun(fimmap)
experiment.solver_config('GFS Fiber Solver')

# Define the optimization problem
creator.create("FitnessMulti", base.Fitness, weights=(-1.0, -1.0, -1.0))
creator.create("Individual", list, fitness=creator.FitnessMulti)

# Configure the optimization problem
toolbox = base.Toolbox()
toolbox.register("individual", initIndividual, creator.Individual, initial_values, list, constraints)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxBlend, alpha=0.5)
toolbox.register("mutate", custom_mutGaussian_constraints, mu=0, sigma=0.8, indpb=0.5, constraints=constraints)
toolbox.register("select", tools.selNSGA2)

# Configure the progress bar, it depends on the:
# initial population(n),
n = 100
# number of individuals selected for the next generation
mu = 50
# offspring from the population (lambda_) and
lambda_ = 100
# number of generations (ngen)
ngen = 20
''''# total iterations (working on)
global global_total
global_total = n + lambda_ * ngen
global global_counter
global_counter = 0'''

# Create the initial population
population = toolbox.population(n)
try:
    # Run the optimization algorithm
    algorithms.eaMuPlusLambda(population, toolbox, mu=mu, lambda_=lambda_, cxpb=0.5, mutpb=0.5, ngen=ngen, stats=None,
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
    header = (['a1', 'dop_a1', 'disp', 'slope', 'dD/dF'])
    # variable to store the data
    data = np.zeros((len(obj1_values), len(header)))
    i = 0
    # Write the data for each individual in the Pareto front into data variable
    for ind in population:
        a1_val, dop_a1_val = ind[0], ind[1]
        obj1_val, obj2_val, obj3_val = ind.fitness.values[0], ind.fitness.values[1], ind.fitness.values[2]
        data[i, :] = [a1_val, dop_a1_val, obj1_val, obj2_val, obj3_val]
        i = i + 1

    data_scan = data.astype('float')
    # add the new row to the top of the array
    data_scan = np.vstack((header, data_scan))

    for element in data_scan:
        f.write(','.join(element) + '\n')
    f.close()

    # Find the solution with the minimum obj1_val and obj2_val above 0.8
    min_obj1_val = float('inf')  # Initialize to positive infinity
    best_solution = None
    # minimum
    thr = 0.08
    thr_dD_fab = 1
    for ind in population:
        obj1_val, obj2_val, obj3_val = ind.fitness.values[0], ind.fitness.values[1], ind.fitness.values[2]
        if obj1_val < min_obj1_val and obj2_val < thr and obj3_val < thr_dD_fab:
            min_obj1_val = obj1_val
            best_solution = ind

    if best_solution:
        print("Best solution with the minimum dispersion and slope bellow 0.08:")
        print("a1:", best_solution[0])
        print("a1_dopa:", best_solution[1])
        print("Dispersion:", best_solution.fitness.values[0])
        print("Slope:", best_solution.fitness.values[1])
        print("dD/dF_0.1um:", best_solution.fitness.values[2])
    else:
        print("No solution found with obj2_val below 0.08")


    # setting FIMMWAVE at the best solution
    sizes[0] = best_solution[0]
    dop_perct[0] = best_solution[1]
    fiber_profile.update_profile(dev, sizes, dop_perct, profile_type, materials, alphas, n_steps)
    wavelength = 1.55
    fiber_profile.set_wavelength(dev, wavelength)

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