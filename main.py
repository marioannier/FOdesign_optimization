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
    fiber_profile.builder_profile(dev, 0.05, 0.05, 0, 0.05, 5.325, 3.302, 4.633, 6, "Step Index", 0)
    fimmap.Exec(dev + ".evlist.mlp.maxnmodes=10")
    dev = "app.subnodes[1].subnodes[2]"
    fiber_profile.builder_profile(dev, 0.05, 0.05, 0, 0.05, 5.325, 3.302, 4.633, 6, "Graded", 1)
    fimmap.Exec(dev + ".evlist.mlp.maxnmodes=10")
    dev = "app.subnodes[1].subnodes[3]"
    fiber_profile.builder_profile(dev, 0.05, 0.05, 0, 0.05, 5.325, 3.302, 4.633, 6, "Graded", 2.2)
    fimmap.Exec(dev + ".evlist.mlp.maxnmodes=10")

# TESTING CHANGING FIBER PARAMETERS
do_we_need_to_updatad_FWG_modules = False
if do_we_need_to_updatad_FWG_modules:
    dev = "app.subnodes[1].subnodes[1]"
    fiber_profile.update_profile(dev, 0.05, 0.05, 0, 0.05, 5.325, 3.302, 4.633, 6, "Step Index", 0)

    dev = "app.subnodes[1].subnodes[2]"
    fiber_profile.update_profile(dev, 0.05, 0.05, 0, 0.05, 5.325, 3.302, 4.633, 6, "Graded", 1)

    dev = "app.subnodes[1].subnodes[3]"
    fiber_profile.update_profile(dev, 0.05, 0.05, 0, 0.05, 5.325, 3.302, 4.633, 6, "Graded", 2.2)

# variables I want to modify: a1, a2, a3, n1, n3
# I want to calculate: mode_values: beta, neff, a_eff, alpha, dispersion, isLeaky, neffg
# and also find this values for different lambdas


want_to_calculate_lambda = True
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
