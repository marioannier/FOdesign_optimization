# asociated to the file 19cores.prj, un proyecto con los cores previamente diseñados

from pdPythonLib import *
from fiber_design import *
from tkinter import filedialog
from tkinter import *

import numpy as np

root = Tk()
root.filename = filedialog.askopenfilename(title="Select file",
                                           filetypes=(("all files", "*.*"), ("Text files", "*.txt")))
root.destroy()

f = open('result.csv', 'w')

# Establishes connection and open the project
fimmap = pdApp()
fimmap.StartApp('C:\\Program Files\\PhotonD\\Fimmwave\\bin64\\fimmwave.exe', 5101)
# open the project
fimmap.Exec("app.openproject(" + root.filename + ")")

fiber_profile = CoreProfile(fimmap)

param_Name = ["lambda"]
lam_s = 1.5
lam_e = 1.6
steps = 1000
data = np.zeros((steps * 16, 9 + 1))


for core_numb in range(1, 17):
    dev = "app.subnodes[1].subnodes[" + str(core_numb) + ']'
    row_ini = (core_numb - 1) * steps
    row_end = core_numb * steps
    data[row_ini:row_end, :] = fiber_profile.scan_lambda(dev, lam_s, lam_e, steps)
    print('Simulation goes for: ' + str(100 * core_numb / 17) + ' %')

# Save the array a to a CSV file
for element in data:
    # Convert elements to strings and join them
    line = ','.join(str(e) for e in element)
    # Write the line to the file
    f.write(line + '\n')


f.close()

del fimmap
