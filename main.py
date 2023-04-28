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
if Is_the_project_created == False:
    # create the profiles
    data_base = 'refbase_2.mat'
    fiber_profile.add_moduleFWG("Step Index", data_base)
    fiber_profile.add_moduleFWG("Triangular", data_base)
    fiber_profile.add_moduleFWG("Graded", data_base)

# FALTA CHEKEAR EL NUMERO DE CAPAS Y CONTRUIR EN DEPENDENCIA DE ELLAS use Exce()
Are_the_FWG_modules_created = False
if Are_the_FWG_modules_created == False:
    max_num_modes = 10
    dev = "app.subnodes[1].subnodes[1]"
    fiber_profile.builder_profile(dev, 0.05, 0.05, 0, 0.05, 5.325, 3.302, 4.633, 6, "Step Index", 0)
    fimmap.Exec(dev + ".evlist.mlp.maxnmodes=10")
    # dev = "app.subnodes[1].subnodes[2]"
    # fiber_profile.builder_profile(dev, 1.46, SiO2_ref_index, 0, 0, 6, 2, 3, 4, "Graded", 1)
    # fimmap.Exec(dev + ".evlist.mlp.maxnmodes=10")
    # dev = "app.subnodes[1].subnodes[3]"
    # fiber_profile.builder_profile(dev, 1.46, SiO2_ref_index, 0, 0, 6, 2, 3, 4, "Graded", 2.2)
    # fimmap.Exec(dev + ".evlist.mlp.maxnmodes=10")

# variables I want to modify: a1, a2, a3, n1, n3
# I want to calculate: mode_values: beta, neff, a_eff, alpha, dispersion, isLeaky, neffg
# and also find this values for different lambdas
# param_Name = ["lambda"]
# param_Scan = ["beta", "neff", "a_eff", "alpha", "dispersion", "isLeaky", "neffg"]
# param_Start = 1.4
# param_End = 1.7
# param_Steps = 4
# scan_Setting = [param_Name, param_Scan, param_Start, param_End, param_Steps]
# data = np.zeros((param_Steps, 7))
# data = data.astype('str')
# # device under test
# dev = "app.subnodes[1].subnodes[2]"
#
# for j in param_Name:
#     print("Scanning " + j + " and extracting: " + ", ".join(param_Scan))
#
#     for i in range(0, param_Steps, 1):
#         step = param_Start + (float(i) / param_Steps) * (param_End - param_Start)
#         print("Solving Modes at " + j + " = " + str(step))
#         fimmap.Exec(dev + ".evlist.svp.lambda=" + str(step))
#         data[i, :] = list(fiber_profile.mode_data(dev, 1, 1, 1, 1, 1, 1, 1).values())
#         f.write(str(data[i, :])) # problem to save the data
# print("All done!")

# Save the array a to a CSV file
# np.savetxt('output.csv', a, delimiter=',')

# Load the saved CSV file and print its contents to verify the save was successful
# loaded_data = np.loadtxt('output.csv', delimiter=',')
# print(loaded_data)
#print(data)

f.close()
del fimmap
