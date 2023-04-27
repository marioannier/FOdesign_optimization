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
SiO2_ref_index = 1.4440236217
dev = "app.subnodes[1].subnodes[1]"
fiber_profile.builder_profile(dev, 1.46, SiO2_ref_index, 0, 0, 6, 2, 3, 4, "Step Index", 0)
dev = "app.subnodes[1].subnodes[2]"
fiber_profile.builder_profile(dev, 1.46, SiO2_ref_index, 0, 0, 6, 2, 3, 4, "Graded", 1)
dev = "app.subnodes[1].subnodes[3]"
fiber_profile.builder_profile(dev, 1.46, SiO2_ref_index, 0, 0, 6, 2, 3, 4, "Graded", 2.2)


# variables I want to modify: a1, a2, a3, n1, n3
# I want to calculate: mode_values: beta, neff, a_eff, alpha, dispersion, isLeaky, neffg
# and also find this values for different lambdas
param_Name = ["lambda"]
param_Scan = ["dispersion"]
param_Start = 1.4
param_End = 1.9
param_Steps = 50
scan_Setting = [param_Name, param_Scan, param_Start, param_End, param_Steps]

# device under test
dev = "app.subnodes[1].subnodes[2]"

for j in param_Name:
    print("Scanning " + j + " and extracting: " + ", ".join(param_Scan))

    for i in range(0, param_Steps + 1, 1):
        step = param_Start + (float(i) / param_Steps) * (param_End - param_Start)
        print("Solving Modes at " + j + " = " + str(step))
        fimmap.Exec(dev + ".evlist.svp.lambda="+str(step))
        fimmap.Exec(dev + ".evlist.update()")
        fimmap.AddCmd(dev + ".evlist.list[1].modedata.update(1)")
        disp = fimmap.Exec(dev + ".evlist.list[1].modedata.dispersion()")
        f.write(str(step) + " ," + str(disp) + "\n")

print("All done!")

f.close()
del fimmap
