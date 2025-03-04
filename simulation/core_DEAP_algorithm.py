import random
import numpy as np

from fiber.core_type import FiberParameters

from collections.abc import Sequence
from itertools import repeat
from deap import base, creator, tools, algorithms


class CoreDEAPAlgorithm:
    MIN_DISPERSION_LIMIT = 0
    MAX_DISPERSION_PENALIZATION = 50
    WORKING_WAVELENGTH = 1.55
    ERR_FAB_MAX = 0.1
    SCALING_STEPS = 3
    PARAMETERS_SCAN = {"beta": True, "neff": True, "a_eff": True, "alpha": True, "dispersion": True,
                       "isLeaky": True, "neffg": True, "fillFac": True, "gammaE": True}

    def __init__(self, fimmap=object, fiber_profile=object, experiment=object, type_index_profile=None):
        self.fimmap = fimmap
        self.fiber_profile = fiber_profile
        self.experiment = experiment
        self.type_index_profile = type_index_profile

    def exponential_penalty_function(self, x, x_optimal, alpha=0.1, lambda_param=0.5):
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

    def feasible(self, individual):
        """
        Feasibility function for the individual. Returns True if feasible, False otherwise.

        Parameters:
        - individual (list): The individual to be checked for feasibility.
        - constraints (list of tuples): List of tuples defining the constraints for each attribute.

        Returns:
        - bool: True if the individual is feasible, False otherwise.
        """
        # Define the constraints for each parameter
        a1 = [(1.5, 5)]
        a2 = [(1.5, 5)]
        a3 = [(1.5, 5)]
        a4 = [(30, 30)]

        dop_a1 = [(0, 0.1)]
        dop_a2 = [(0, 0.1)]
        dop_a3 = [(0, 0.1)]
        dop_a4 = [(0, 0)]

        alpha_a1 = [(0, 2)]
        alpha_a2 = [(0, 0)]
        alpha_a3 = [(0, 0)]
        alpha_a4 = [(0, 0)]

        constraints = a1 + a2 + a3 + dop_a1 + dop_a2 + dop_a3

        for i, (min_value, max_value) in enumerate(constraints):
            if not (min_value <= individual[i] <= max_value):
                return False
        return True

    def distance(self, individual):
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

        a1 = [(1.5, 5)]
        a2 = [(1.5, 5)]
        a3 = [(1.5, 5)]
        a4 = [(30, 30)]

        dop_a1 = [(0, 0.1)]
        dop_a2 = [(0, 0.1)]
        dop_a3 = [(0, 0.1)]
        dop_a4 = [(0, 0)]

        alpha_a1 = [(0, 2)]
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

    def objective_function_dispersion(self, parameters):
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
        param = core_type.core_type_meth(self.type_index_profile)

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
        self.fiber_profile.update_profile(dev, sizes, dop_perct, profile_type,
                                          materials, alphas, n_steps)

        # Running simulation
        # get the data for the 1rst and 2nd LP modes;
        # since we configure both polarizations, the 2nd mode corresponds to '3'

        data_mode1 = self.experiment.simulate(self.PARAMETERS_SCAN, mode='1')
        data_mode3 = self.experiment.simulate(self.PARAMETERS_SCAN, mode='3')

        # get the dispersion value for mode 1 and the guided status of mode 1 nad 2
        dispersion_mode1 = data_mode1[4]
        is_leaky_mode1 = data_mode1[5]
        is_leaky_mode2 = data_mode3[5]

        # getting the confinement factor value
        confinement_factor = data_mode1[7]

        # Penalization
        if is_leaky_mode1 == 1 or is_leaky_mode2 == 2:
            dispersion_mode1 = self.MAX_DISPERSION_PENALIZATION

        #OJO DETERMINAR EL VALOR DEL confinement_factor CORRECO, 0.5 ES UN APROX
        if confinement_factor < 0.5:
            dispersion_mode1 = self.MAX_DISPERSION_PENALIZATION

        if dispersion_mode1 < -500:
            dispersion_mode1 = self.MAX_DISPERSION_PENALIZATION

        return dispersion_mode1

    def objective_function_slope(self, parameters):
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
        param = core_type.core_type_meth(self.type_index_profile)

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
        self.fiber_profile.update_profile(dev, sizes, dop_perct, profile_type,
                                          materials, alphas, n_steps)

        # Define wavelength range and the sampling interval (lam_e-lam_s)/number_steps
        number_steps = 4
        lam_s = 1.53
        lam_e = 1.56
        steps = np.linspace(lam_s, lam_e, number_steps)

        # Running simulation
        # get the data for the 1rst mode;
        data_mode1 = np.zeros((number_steps, 9))

        # Iterate over all scaling values
        for i, wavelength in enumerate(steps):
            # setting the work wavelength
            self.fiber_profile.set_wavelength(dev, wavelength)
            # running simulation
            data_mode1[i, :] = self.experiment.simulate(self.PARAMETERS_SCAN, mode='1')

        # setting to 1.55 at the end of the analysis
        self.fiber_profile.set_wavelength(dev, self.WORKING_WAVELENGTH)

        # Calculate the derivative of dispersion with respect to wavelength
        slope = np.diff(data_mode1[:, 4]) / np.diff(steps * 1000)  # transform the wavelength to nm

        # Calculate the average slope
        slope_ave = np.average(slope)
        output = np.abs(slope_ave)

        # bound the objetive function
        #if output > 2 or output == 0:
        #output = 60

        return output

    def objective_function_err_fab(self, parameters):
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

        # Initial parameters, defining the core type
        core_type = FiberParameters()

        # Getting the standard constructive parameters for the study core profile
        param = core_type.core_type_meth(self.type_index_profile)

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
        rep_factor_scala = self.ERR_FAB_MAX / a1
        # Then I find the scaling factor values
        steps = np.linspace(1 - rep_factor_scala, 1 + rep_factor_scala, self.SCALING_STEPS)
        data_mode1 = np.zeros((self.SCALING_STEPS, 9))

        # determine the dispersion for each factor of scale from -ERR_FAB_MAX to ERR_FAB_MAX
        for i, sca_fact in enumerate(steps):
            sizes[0] = a1 * sca_fact
            sizes[1] = a2 * sca_fact
            sizes[2] = a3 * sca_fact
            self.fiber_profile.update_profile(dev, sizes, dop_perct, profile_type, materials, alphas, n_steps)
            # running simulation
            data_mode1[i, :] = self.experiment.simulate(self.PARAMETERS_SCAN, mode='1')

        # Calculate the derivative of dispersion with respect to an ERR_FAB_MAX
        scaling_intervals = 2 * self.ERR_FAB_MAX / (self.SCALING_STEPS - 1)
        fac = self.ERR_FAB_MAX / scaling_intervals
        diff_err_fab = fac * np.diff(data_mode1[:, 4])

        # determining the absolute value
        output = np.abs(np.average(diff_err_fab))

        # bound the objetive function
        #if output > 5 or output == 0:
        #output = 60

        return output

    def evaluate(self, individual):
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
        disp = self.objective_function_dispersion(individual)
        obj1 = disp

        # Objective 2 calculation
        slope = self.objective_function_slope(individual)
        obj2 = slope

        # Objective 3 calculation
        dif_fab_err = self.objective_function_err_fab(individual)
        obj3 = dif_fab_err

        return obj1, obj2, obj3

    # Function to initialize individuals
    def initIndividual(self, icls, content, ccls, constraints):
        """Initialize an individual with random values within constraints, ensuring
            dop_a3 ∈ [0, dop_a1].

            :param icls: Class used to instantiate the individual
            :param content: Container for individual attributes
            :param ccls: Class used for crossover/mutation compatibility (unused)
            :param constraints: List of (min, max) tuples defining value ranges for parameters.
                                Format: [a1, a2, a3, dop_a1, dop_a2, dop_a3]
            :returns: Initialized individual with parameters within constraints

            Special handling:
            - For dop_a3 (6th parameter): Overrides its constraints to use [0, current dop_a1]
            - Fixed parameters (where min==max) will use the exact specified value
            - Uses :func:`~random.uniform` for value generation

            Example constraints structure:
            constraints = [
                (1.5, 5),    # a1
                (1.5, 5),    # a2
                (1.5, 5),    # a3
                (0.01, 0.15),# dop_a1
                (0, 0),      # dop_a2
                (0.001, 0.1) # dop_a3 (constraint ignored)
            ]
            """

        part = icls(content)
        for i, (min_value, max_value) in enumerate(constraints):
            if i == 5:  # dop_a3 is the 6th parameter (index 5)
                # Ensure dop_a3 ∈ [0, current 95% of dop_a1 value]
                part[i] = random.uniform(0, part[3]- 0.05 * part[3])
            else:
                # Use original constraints for other parameters
                part[i] = random.uniform(min_value, max_value)
            part[i] = round(part[i], 3)
        return part

    def custom_mutGaussian_constraints(self, individual, mu, sigma, indpb, constraints):
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
        #print(f'sigma: {sigma}')
        size = len(individual)
        if not isinstance(mu, Sequence):
            mu = repeat(mu, size)
        elif len(mu) < size:
            raise IndexError("mu must be at least the size of individual: %d < %d" % (len(mu), size))
        if not isinstance(sigma, Sequence):
            sigma = repeat(sigma, size)
        elif len(sigma) < size:
            raise IndexError("sigma must be at least the size of individual: %d < %d" % (len(sigma), size))

        """Applies Gaussian mutation while enforcing dop_a3 ∈ [0, dop_a1]."""
        for i, m, s, (orig_min, orig_max) in zip(range(size), mu, sigma, constraints):
            # Override constraints for dop_a3 (index 5)
            if i == 5:
                current_min = 0  # Force minimum 0 for dop_a3
                current_max = individual[3] - 0.05 * individual[3]  # Dynamic max from 95% of dop_a1 (index 3)
            else:
                current_min, current_max = orig_min, orig_max
            if random.random() < indpb:
                mutated_value = individual[i] + random.gauss(m, s)
                individual[i] = max(min(mutated_value, current_max), current_min)
            else:
                individual[i] = max(min(individual[i], current_max), current_min)
            individual[i] = round(individual[i], 3)
        return individual

    def algorithm_execution(self, n=20, mu=10, lambda_=15, ngen=10, initial_values=0, mean_d=0, sigma=0.9, indpb=0.5,
                            constraints=0):

        # CREATE THE HELP TO THE FUNCTION

        # Configure the progress bar, it depends on the:
        # n initial population(n),
        # mu number of individuals selected for the next generation
        # lambda_ offspring from the population (lambda_) and
        # ngen number of generations (ngen)

        try:
            # Define the optimization problem
            creator.create("FitnessMulti", base.Fitness, weights=(-1.0, -1.0, -1.0))
            creator.create("Individual", list, fitness=creator.FitnessMulti)

            # Configure the optimization problem
            toolbox = base.Toolbox()
            toolbox.register("individual", self.initIndividual, creator.Individual, initial_values, list, constraints)
            toolbox.register("population", tools.initRepeat, list, toolbox.individual)
            toolbox.register("evaluate", self.evaluate)
            toolbox.decorate("evaluate", tools.DeltaPenalty(self.feasible, (30, 3, 3), self.distance))
            toolbox.register("mate", tools.cxBlend, alpha=0.5)
            toolbox.register("mutate", self.custom_mutGaussian_constraints, mu=mean_d, sigma=sigma, indpb=indpb,
                             constraints=constraints)
            toolbox.register("select", tools.selNSGA2)

            logbook = tools.Logbook()

            # Create the initial population
            population = toolbox.population(n)

            # Create a Statistics object and register the desired statistics
            stats = tools.Statistics(lambda ind: ind.fitness.values)
            stats.register("min", np.min, axis=0)
            stats.register("max", np.max, axis=0)
            stats.register("avg", np.mean, axis=0)
            stats.register("std", np.std, axis=0)

            # Run the optimization algorithm with stats
            _, logbook = algorithms.eaMuPlusLambda(population, toolbox, mu=mu, lambda_=lambda_, cxpb=0.5, mutpb=0.5,
                                                   ngen=ngen,
                                                   stats=stats,
                                                   halloffame=None, verbose=True)

        except Exception as e:
            # Handle the exception
            print(f'An error occurred in core_DEAP_algorithm: {str(e)}')

        finally:
            return population
