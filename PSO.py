import numpy as np
from fiber_design import *
from tkinter import *
from tkinter import filedialog
import fimmwavelib as fimm


# Define the objective function
def objective_function(a):
    # Unpack the variables
    a1, a2, a3, a4, dop1, dop2, dop3, dop4 = a

    dev = "app.subnodes[1].subnodes[4]"
    fiber_p = 'Triangular T'
    alpha_val = 1
    fiber_profile.update_profile(dev, a1, a2, a3, a4, dop1, dop2, dop3, dop4, fiber_p, alpha_val)
    mode_data = fiber_profile.mode_data(dev)

    # Calculate the value to minimize (disp)
    disp = mode_data[4]  # Replace with the function that calculates disp
    print(disp)
    if disp < 0:
        disp = 100

    return disp


# Define the bounds for each variable
# bounds = [(4, 6)] * 4 + [(0, 0.07)] * 4
bounds = [(4, 6)] * 3 + [(30, 30)] + [(0, 0.07)] + [(0, 0)] + [(0, 0)] + [(0, 0)]


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


# Set the parameters for the PSO algorithm
num_particles = 10
max_iterations = 10

# getting the project directory
root = Tk()
root.filename = filedialog.askopenfilename(title="Select file",
                                           filetypes=(("all files", "*.*"), ("Text files", "*.txt")))
root.destroy()  # Close the window

# Establishing the connection with FIMMWAVE
fimmap = pdApp()
fimmap.StartApp('C:\\Program Files\\PhotonD\\Fimmwave\\bin64\\fimmwave.exe', 5101)
fimmap.Exec("app.openproject(" + root.filename + ")")
# create the object
fiber_profile = CoreProfile(fimmap)

# Run the PSO algorithm
best_solution = pso(objective_function, bounds, num_particles, max_iterations)

# Extract the best values for each variable
best_a1, best_a2, best_a3, best_a4, best_dop1, best_dop2, best_dop3, best_dop4 = best_solution

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

min_disp = objective_function(best_solution)
print("Minimum Disp:", min_disp)
