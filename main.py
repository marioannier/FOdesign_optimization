from pdPythonLib import *
from fiber_design import *
from core_profile_index_builder import *
import fiber_profile_gen as fp

import numpy as np
import fimmwavelib as fimm
'''
fimmap = pdApp()
fimmap.StartApp('C:\\Program Files\\PhotonD\\Fimmwave\\bin64\\fimmwave.exe', 5101)

test_dir = 'D:\\OneDrive UPV\\OneDrive - UPV\PhD-m\\2023-2024\\FiberDesin_PhotonD\\FOdesign_optimization'
fiber_profile = ProfileIndexBuilder(fimmap)
fiber_profile.create_fimm_project('test2', test_dir)
fiber_profile.add_moduleFWG('Module 1')

dev = "app.subnodes[1].subnodes[1]"
sizes = [5, 2, 3]
dop_perct = [0.5, 0, 0.2]
profile_type = ['Graded', 'Contant', 'Raised cosine']
materials = ['GeO2-SiO2', 'SiO2', 'GeO2-SiO2']
alpha = [2, 0, 1]
n_steps = 100

fiber_profile.builder_profile(dev, sizes, dop_perct, profile_type, materials, alpha, n_steps)

del fimmap
'''