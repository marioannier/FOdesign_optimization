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
f = open('D_C7.csv', 'w')
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
dev = "app.subnodes[1].subnodes[1]"
fiber_profile.builder_profile(dev, 1.5, 1.4, 0, 0, 1, 2, 3, 4, "Step Index", 0)
