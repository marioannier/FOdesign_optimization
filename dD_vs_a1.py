# asociated to the file 19cores.prj, un proyecto con los cores previamente diseñados

from pdPythonLib import *
from FiberProfile import *
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

fiber_profile = FiberProfile(fimmap)

table_a1 = [3.316516517, 3.541141141, 3.861561562, 4.026726727, 4.208408408, 4.551951952, 4.305105105, 4.460660661,
            4.628828829, 4.796996997, 5.057657658, 3.615615616, 3.706706707, 3.874874875, 4.523023023, 6.656656657]
table_a2 = [4.512472472, 4.818098098, 5.254064064, 5.478788789, 5.725985986, 6.193413413, 1.23003003, 1.274474474,
            1.322522523, 1.370570571, 1.445045045, 2.169369369, 2.224024024, 2.324924925, 2.713813814, 3.993993994]
table_a3 = [1.306506507, 1.394994995, 1.521221221, 1.586286286, 1.657857858, 1.793193193, 1.537537538, 1.593093093,
            1.653153153, 1.713213213, 1.806306306, 3.099099099, 3.177177177, 3.321321321, 3.876876877, 5.705705706]
table_n1 = [0.075, 0.075, 0.075, 0.075, 0.075, 0.075, 0.04, 0.04, 0.04, 0.04, 0.04, 0.04, 0.04, 0.04, 0.04, 0.04]
alpha = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1]
fiber_p = ["Triangular", "Triangular", "Triangular", "Triangular", "Triangular", "Triangular", "Graded", "Graded",
           "Graded", "Graded", "Graded", "Step Index", "Step Index", "Step Index", "Step Index", "Step Index"]
core = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16"]

a1_s = -0.2
a1_e = 0.2
steps = 50
step = np.linspace(a1_s, a1_e, steps)

data_scan = np.zeros((steps * 16, 2 + 9))

for core_numb in range(1, 17):
    dev = "app.subnodes[1].subnodes[" + str(core_numb) + ']'
    # row_ini = (core_numb - 1) * steps
    # row_end = core_numb * steps
    # data[row_ini:row_end, :] = fiber_profile.scan_lambda(dev, lam_s, lam_e, steps)
    for i in range(0, steps):
        a1 = table_a1[core_numb - 1] + step[i]
        fiber_profile.update_profile(dev, a1, table_a2[core_numb - 1], table_a3[core_numb - 1], 15,
                                     table_n1[core_numb - 1],
                                     0, 0, 0, fiber_p[core_numb - 1], alpha[core_numb - 1])
        data_scan[(core_numb - 1) * steps + i, 2:] = list(fiber_profile.mode_data(dev))
        data_scan[(core_numb - 1) * steps + i, 0:2] = [core[core_numb - 1], a1]

# Save the array a to a CSV file
for element in data_scan:
    # Convert elements to strings and join them
    line = ','.join(str(e) for e in element)
    # Write the line to the file
    f.write(line + '\n')

f.close()

del fimmap
