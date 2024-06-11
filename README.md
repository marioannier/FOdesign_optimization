# Fiber Design Optimization

This repository contains a Python project that uses a genetic algorithm to optimize the design parameters of an optical fiber with a specific refractive index profile. The goal is to minimize dispersion, slope of dispersion, and differential dispersion per fabrication error (dD/dF_0.1um) for a triangular profile with a ring.

## Table of Contents
- [Introduction](#introduction)
- [Setup](#setup)
- [Usage](#usage)
- [Files and Directories](#files-and-directories)
- [Functions and Methods](#functions-and-methods)
- [Results](#results)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This project uses the DEAP (Distributed Evolutionary Algorithms in Python) library to perform multi-objective optimization on the design parameters of an optical fiber. The specific objectives are to minimize the following:
- Dispersion
- Slope of dispersion
- Differential dispersion per fabrication error (dD/dF_0.1um)

## Setup

### Prerequisites

- Python 3.8 or later
- DEAP library
- NumPy
- Matplotlib
- mplcursors
- FIMMWAVE software (for fiber simulations)

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/fiber-design-optimization.git
    cd fiber-design-optimization
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

3. Ensure FIMMWAVE is installed and the path to its executable is correct in the code.

## Usage

1. **Configure the paths:**

   Modify the path variables in the code to match your working environment. Specifically, update the `test_dir` variable to point to the directory where your fiber design files are located.

2. **Run the optimization:**

    ```bash
    python optimize_fiber.py
    ```

3. **View Results:**

   After the optimization completes, results will be saved in a CSV file named `Pareto_fron_trieangular_trench_F-SiO2_1_<timestamp>.csv`. A 3D plot of the Pareto front will also be displayed.

## Files and Directories

- `optimize_fiber.py`: Main script to run the optimization.
- `requirements.txt`: List of required Python packages.
- `core_profile_index_builder.py`: Module for building fiber index profiles.
- `simulation_run.py`: Module for running fiber simulations.
- `core_type.py`: Module defining fiber parameters and profiles.
- `pdPythonLib.py`: Custom library for interacting with FIMMWAVE.

## Functions and Methods

### Main Functions

- `exponential_penalty_function(x, x_optimal, alpha, lambda_param)`: Computes an exponential penalty based on deviation from optimal values.
- `feasible(individual)`: Checks if an individual is within the defined constraints.
- `distance(individual)`: Computes the quadratic distance from the feasibility region.
- `objective_function_dispersion(parameters)`: Calculates the dispersion for given fiber parameters.
- `objective_function_slope(parameters)`: Calculates the slope of dispersion for given fiber parameters.
- `objective_function_err_fab(parameters)`: Calculates the differential dispersion per fabrication error for given fiber parameters.
- `evaluate(individual)`: Evaluates an individual by combining the three objective functions.
- `initIndividual(icls, content, ccls, constraints)`: Initializes individuals with random values within constraints.
- `custom_mutGaussian_constraints(individual, mu, sigma, indpb, constraints)`: Applies Gaussian mutation while respecting constraints.

### Main Execution

- **Setup**: Initializes DEAP's genetic algorithm components and FIMMWAVE simulation environment.
- **Optimization**: Runs the genetic algorithm to evolve the population over generations.
- **Post-Optimization**: Handles results, updates the fiber profile, and visualizes the Pareto front.

## Results

Results are saved in a CSV file and plotted as a 3D Pareto front. The CSV file contains:
- Parameters of the fiber design (a1, a2, a3, dop_a1, dop_a3)
- Objective values (dispersion, slope, dD/dF)

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
