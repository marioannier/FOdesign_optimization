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

    #   param_Scan = {"beta": False, "neff": False, "a_eff": False, "alpha": False, "dispersion": True,
    #               "isLeaky": False, "neffg": False}
    #
    # for j in param_Name:
    #     print("Scanning " + j + " and extracting: " + ", ".join(param_Scan2))
    #
    #     for i in range(0, param_Steps, 1):
    #         step = param_Start + (float(i) / param_Steps) * (param_End - param_Start)
    #         print("Solving Modes at " + j + " = " + str(step))
    #         fimmap.Exec(dev + ".evlist.svp.lambda=" + str(step))
    #         data[i, :] = list(fiber_profile.mode_data(dev, param_Scan))
    #         f.write(str(data[i, :]))  # problem to save the data
    # print("All done!")

# # Save the array a to a CSV file
# np.savetxt('output.csv', a, delimiter=',')
#
# # Load the saved CSV file and print its contents to verify the save was successful
# loaded_data = np.loadtxt('output.csv', delimiter=',')
# print(loaded_data)
# print(data)


f.close()
del fimmap
