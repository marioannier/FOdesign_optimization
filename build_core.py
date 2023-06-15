# asociated to the file build_profile.prj, un proyecto vacio

from pdPythonLib import *
from FiberProfile import *
from tkinter import filedialog
from tkinter import *

import numpy as np

root = Tk()
root.filename = filedialog.askopenfilename(title="Select file",
                                           filetypes=(("all files", "*.*"), ("Text files", "*.txt")))
root.destroy()

# Establishes connection and open the project
fimmap = pdApp()
fimmap.StartApp('C:\\Program Files\\PhotonD\\Fimmwave\\bin64\\fimmwave.exe', 5101)
# dir = '(D:\\OneDrive UPV\\OneDrive - UPV\\PhD-m\\2022-2023\\lines\\Nonuniformly Spaced Photonic
# Microwave\\Simulations_run\\FIMMWAVE_Python\\FOdesign_optimization\\Experiment_fibers.prj,"")';
fimmap.Exec("app.openproject(" + root.filename + ")")

fiber_profile = FiberProfile(fimmap)

data_base = 'refbase_2.mat'
core_type = "Graded"  # INSERT
fiber_profile.add_moduleFWG(core_type, data_base)
dev = "app.subnodes[1].subnodes[1]"

# INSERT
a1 = 5.05765765765765
a2 = 1.44504504504504
a3 = 1.8063063063063
a4 = 10
n1_dopant = 0.1
n2_dopant = 0
n3_dopant = 0
n4_dopant = 0
alpha = 1.0

fiber_profile.builder_profile(dev, a1, a2, a3, a4, n1_dopant, n2_dopant, n3_dopant, n4_dopant, core_type, alpha)

del fimmap
