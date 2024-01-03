import customtkinter
import numpy as np
import time

from fiber_design import *
from tkinter import *
from fiber_design import *
from simulation_run import *
from core_profile_index_builder import *

fimmap = pdApp()
fimmap.StartApp('C:\\Program Files\\PhotonD\\Fimmwave\\bin64\\fimmwave.exe', 5101)

# from work
test_dir = 'D:\\OneDrive UPV\\OneDrive - UPV\PhD-m\\2023-2024\\FiberDesin_PhotonD\\FOdesign_optimization'
# from personal computer
test_dir = 'C:\\Users\\Mario\OneDrive - UPV\PhD-m\\2023-2024\\FiberDesin_PhotonD\\FOdesign_optimization'
fiber_profile = ProfileIndexBuilder(fimmap)
fiber_profile.create_fimm_project('test2', test_dir)
fiber_profile.add_moduleFWG('Module 1')
fiber_profile.set_material_db(test_dir, 'refbase_2.mat')
dev = "app.subnodes[1].subnodes[1]"
sizes = [5, 2, 3, 4, 19]
dop_perct = [0.5, 0, 0.2, 0.8, 0]
profile_type = ['Contant', 'Contant', 'Contant', 'Contant', 'Contant']
materials = ['GeO2-SiO2', 'GeO2-SiO2', 'GeO2-SiO2', 'GeO2-SiO2', 'GeO2-SiO2']
alpha = [2, 0, 1, 0, 0]
n_steps = 100

fiber_profile.builder_profile(dev, sizes, dop_perct, profile_type, materials, alpha, n_steps)
# simulation
experiment = SimulationRun(fimmap)
experiment.solver_config('FDM Fiber Solver')

param_Scan = {"beta": True, "neff": True, "a_eff": True, "alpha": True, "dispersion": True, "isLeaky": True,
              "neffg": True, "fillFac": True, "gammaE": True}

data = experiment.simulate(param_Scan, mode='1')
print(data)

del fimmap
