from pdPythonLib import *
from FiberProfile import *
from tkinter import filedialog
from tkinter import *

import numpy as np
import matplotlib.pyplot as plt
import fimmwavelib as fimm

# get the project directory (project) FALTA HACER UN IF PARA CREAR EL PROJECTO O ABRIR EL YA EXISTENTE
root = Tk()
root.filename = filedialog.askopenfilename(title="Select file",
                                           filetypes=(("all files", "*.*"), ("Text files", "*.txt")))
root.destroy()  # Close the window

# Establishes connection and open the project
f = open('result.csv', 'w')
fimmap = pdApp()
fimmap.StartApp('C:\\Program Files\\PhotonD\\Fimmwave\\bin64\\fimmwave.exe', 5101)
# dir = '(D:\\OneDrive UPV\\OneDrive - UPV\\PhD-m\\2022-2023\\lines\\Nonuniformly Spaced Photonic
# Microwave\\Simulations_run\\FIMMWAVE_Python\\FOdesign_optimization\\Experiment_fibers.prj,"")';
fimmap.Exec("app.openproject(" + root.filename + ")")

fiber_profile = FiberProfile(fimmap)

Is_the_project_created = True
if not Is_the_project_created:
    # create the profiles
    data_base = 'refbase_2.mat'
    fiber_profile.add_moduleFWG("Step Index", data_base)
    fiber_profile.add_moduleFWG("Triangular", data_base)
    fiber_profile.add_moduleFWG("Graded", data_base)

# FALTA CHEKEAR EL NUMERO DE CAPAS Y CONTRUIR EN DEPENDENCIA DE ELLAS use Exce()
Are_the_FWG_modules_created = True
if not Are_the_FWG_modules_created:
    max_num_modes = 10
    dev = "app.subnodes[1].subnodes[1]"
    fiber_profile.builder_profile(dev, 5.325, 3.302, 4.633, 6, 0.05, 0.05, 0, 0.05, "Step Index", 0)
    fimmap.Exec(dev + ".evlist.mlp.maxnmodes=10")
    dev = "app.subnodes[1].subnodes[2]"
    fiber_profile.builder_profile(dev, 5.325, 3.302, 4.633, 6, 0.05, 0.05, 0, 0.05, "Graded", 1)
    fimmap.Exec(dev + ".evlist.mlp.maxnmodes=10")
    dev = "app.subnodes[1].subnodes[3]"
    fiber_profile.builder_profile(dev, 5.325, 3.302, 4.633, 6, 0.05, 0.05, 0, 0.05, "Graded", 2.2)
    fimmap.Exec(dev + ".evlist.mlp.maxnmodes=10")

# TESTING CHANGING FIBER PARAMETERS
do_we_need_to_updatad_FWG_modules = False
if do_we_need_to_updatad_FWG_modules:
    dev = "app.subnodes[1].subnodes[1]"
    fiber_profile.update_profile(dev, 5.325, 3.302, 4.633, 6, 0.05, 0.05, 0, 0.05, "Step Index", 0)

    dev = "app.subnodes[1].subnodes[2]"
    fiber_profile.update_profile(dev, 5.325, 3.302, 4.633, 6, 0.05, 0.05, 0, 0.05, "Graded", 1)

    dev = "app.subnodes[1].subnodes[3]"
    fiber_profile.update_profile(dev, 0.05, 5.325, 3.302, 4.633, 6, 0.05, 0, 0.05, "Graded", 2.2)

# variables I want to modify: a1, a2, a3, n1, n3
# I want to calculate: mode_values: beta, neff, a_eff, alpha, dispersion, isLeaky, neffg
# and also find this values for different lambdas
a1_lower = 3
a1_upper = 6
# Define the ranges for each parameter
a1_steps = 5
a1 = np.linspace(a1_lower, a1_upper, a1_steps)  # for a1_steps = 1 , a1 = a1_lower

a2_lower = 2
a2_upper = 3.5
# Define the ranges for each parameter
a2_steps = 1
a2 = np.linspace(a2_lower, a2_upper, a2_steps)

a3_lower = 2.5
a3_upper = 5
# Define the ranges for each parameter
a3_steps = 1
a3 = np.linspace(a3_lower, a3_upper, a3_steps)

a4 = 5

n1 = None
n1_dopant_lower = 0.04
n1_dopant_upper = 0.05
# Define the ranges for each parameter
n1_dopant_steps = 5
n1_dopant = np.linspace(n1_dopant_lower, n1_dopant_upper, n1_dopant_steps)

n2 = None
n2_dopant_lower = 0
n2_dopant_upper = 0
# Define the ranges for each parameter
n2_dopant_steps = 1
n2_dopant = np.linspace(n2_dopant_lower, n2_dopant_upper, n2_dopant_steps)

n3 = None
n3_dopant_lower = 0.001
n3_dopant_upper = 0.001
# Define the ranges for each parameter
n3_dopant_steps = 1
n3_dopant = np.linspace(n3_dopant_lower, n3_dopant_upper, n3_dopant_steps)

n4 = None
n4_dopant_lower = 0
n4_dopant_upper = 0
# Define the ranges for each parameter
n4_dopant_steps = 1
n4_dopant = np.linspace(n4_dopant_lower, n4_dopant_upper, n4_dopant_steps)

alpha_lower = 1
alpha_upper = 3
# Define the ranges for each parameter
alpha_steps = 1
alpha = np.linspace(alpha_lower, alpha_upper, alpha_steps)

# creating variable to store the result
steps = a1_steps * a2_steps * a3_steps * n1_dopant_steps * n2_dopant_steps * n3_dopant_steps * n4_dopant_steps * alpha_steps
data_scan = np.zeros((steps, 7 + 9))  # 7-> max output of fiber_profile.mode_data() and 9 -> number of fiber parameters
i = 0

param_Scan = {"beta": False, "neff": False, "a_eff": False, "alpha": False, "dispersion": True, "isLeaky": True,
              "neffg": False}
header = (
    ['a1(um)', 'a2(um)', 'a3(um)', 'a4(um)', 'n1 dopant(%)', 'n2 dopant(%)', 'n3 dopant(%)', 'n4 dopant(%)', 'alpha',
     "beta", "neff", "a_eff", "alpha", "dispersion", "isLeaky", "neffg"])

dev = "app.subnodes[1].subnodes[2]"

# Iterate over all combinations of parameters
for a1_val in a1:
    for a2_val in a2:
        for a3_val in a3:
            for n1_dopant_val in n1_dopant:
                for n2_dopant_val in n2_dopant:
                    for n3_dopant_val in n3_dopant:
                        for n4_dopant_val in n4_dopant:
                            for alpha_val in alpha:
                                print(
                                    f"Scanning for a1 = {a1_val}, a2 = {a2_val}, a3 = {a3_val}, a4 = {a4}, n1_dopant ="
                                    f" {n1_dopant_val}, n2_dopant = {n2_dopant_val}, n3_dopant = {n3_dopant_val}, "
                                    f"n4_dopant = {n4_dopant_val}, alpha = {alpha_val}")
                                print("and extracting: " + ", ".join([key for key, val in param_Scan.items() if val]))
                                # running the simulation
                                fiber_profile.update_profile(dev, a1_val, a2_val, a3_val, a4, n1_dopant_val,
                                                             n2_dopant_val, n3_dopant_val, n4_dopant_val,
                                                             "Graded", alpha_val)
                                data_scan[i, 9:] = list(fiber_profile.mode_data(dev, param_Scan))
                                data_scan[i, 0:9] = [a1_val, a2_val, a3_val, a4, n1_dopant_val,
                                                     n2_dopant_val, n3_dopant_val, n4_dopant_val,
                                                     alpha_val]
                                i = i + 1
data_scan = data_scan.astype('str')
# add the new row to the top of the array
data_scan = np.vstack((header, data_scan))

for element in data_scan:
    f.write(','.join(element) + '\n')

want_to_calculate_lambda = False
if want_to_calculate_lambda:
    param_Name = ["lambda"]
    param_Scan2 = ["beta", "neff", "a_eff", "alpha", "dispersion", "isLeaky", "neffg"]  # quitar el 2
    lam_s = 1.4
    lam_e = 1.7
    steps = 10

    dev = "app.subnodes[1].subnodes[1]"
    data = np.zeros((steps, 7 + 1))
    data.astype('str')

    data = fiber_profile.scan_lambda(dev, lam_s, lam_e, steps)
    print(data)

    # Save the array a to a CSV file
    for element in data:
        f.write(','.join(element) + '\n')

f.close()
del fimmap
