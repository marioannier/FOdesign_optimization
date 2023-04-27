from pdPythonLib import *
from FiberProfile import *
import numpy as np
import matplotlib.pyplot as plt
import fimmwavelib as fimm

f = open('D_C7.csv', 'w')
fimmap = pdApp()
fimmap.StartApp('C:\\Program Files\\PhotonD\\Fimmwave\\bin64\\fimmwave.exe', 5101)
dir = '(D:\\OneDrive UPV\\OneDrive - UPV\\PhD-m\\2022-2023\\lines\\Nonuniformly Spaced Photonic Microwave\\Simulations_run\\FIMMWAVE_Python\\FOdesign_optimization\\Experiment_fibers.prj,"")';
fimmap.Exec("app.openproject" + dir)
########################################################################################################
# Variation of step index example, lambda parameter
# Calculation of dispersion vs lambda

# varParam1 = "app.subnodes[1].subnodes[5]" # module with variables
# param1name = "lambda"
# param1Start = 1.4
# param1End = 1.9
# param1Steps = 50
#
# print("Scanning " + param1name + " and extracting the propagation constant")
#
# dev = "app.subnodes[1].subnodes[2]" # module under test
#
# for param1 in range(0, param1Steps + 1, 1):
#     param1Value = param1Start + (float(param1) / param1Steps) * (param1End - param1Start)
#     print("Solving Modes at " + param1name + " = " + str(param1Value))
#     fimmap.AddCmd(varParam1 + ".setvariable(" + param1name + "," + str(param1Value) + ")")
#     fimmap.Exec(dev + ".evlist.update()")
#     fimmap.AddCmd(dev + ".evlist.list[1].modedata.update(1)")
#     disp = fimmap.Exec(dev + ".evlist.list[1].modedata.dispersion()")
#     f.write(str(param1Value) + " ," + str(disp) + "\n")
#
# print("All done!")
#

######################################################################################################################
# Variation of step index example, not all parameters (central layer dopant and thickness)
# Calculation of dispersion vs combination -> central layer dopant and thickness

# varParam1 = "app.subnodes[1].subnodes[5]"
# param1name = "n1" # core dopant
# param1Start = 0.08
# param1End = 0.09
# param1Steps = 10
#
# varParam2 = "app.subnodes[1].subnodes[5]"
# param2name = "a2" #thickness
# param2Start = 2
# param2End = 6
# param2Steps = 16
#
# print("Scanning " + param1name + " and " + param2name + " and extracting dispersion, group index and effective index")
#
#
# dev = "app.subnodes[1].subnodes[2]"
#
# for param1 in range(0, param1Steps + 1, 1):
#     param1Value = param1Start + (float(param1) / param1Steps) * (param1End - param1Start)
#     print("Solving Modes at " + param1name + " = " + str(param1Value) + " and")
#     fimmap.AddCmd(varParam1 + ".setvariable(" + param1name + "," + str(param1Value) + ")")
#     for param2 in range(0, param2Steps + 1, 1):
#         param2Value = param2Start + (float(param2) / param2Steps) * (param2End - param2Start)
#         print("    " + param2name + " = " + str(param2Value))
#         fimmap.AddCmd(varParam2 + ".setvariable(" + param2name + "," + str(param2Value) + ")")
#         fimmap.Exec(dev + ".evlist.update")
#         neff = fimmap.Exec(dev + ".evlist.list[1].neff")
#         fimmap.AddCmd(dev + ".evlist.list[1].modedata.update(1)")
#         GRidx = fimmap.Exec(dev + ".evlist.list[1].modedata.neffg")
#         disp = fimmap.Exec(dev + ".evlist.list[1].modedata.dispersion")
#         f.write(str(param1Value) + " ," + str(param2Value) + " ," + str(disp) + " ," + str(GRidx) + "," + str(neff) + "\n")
#
# print("All done!")

##################################################################################################################
# Variation of graded index example, not all parameters -> TRIANGULAR
# Variation of step index example, not all parameters (central layer thickness)
# Calculation of dispersion vs central layer thickness

# varParam1 = "app.subnodes[1].subnodes[5]" # module with variables
# param1name = "a1_graded"
# param1Start = 0.04
# param1End = 0.16
# param1Steps = 10
#
# print("Scanning " + param1name + " and extracting the propagation constant")
#
# dev = "app.subnodes[1].subnodes[4]" # module under test (triangular)
#
# for param1 in range(0, param1Steps + 1, 1):
#     param1Value = param1Start + (float(param1) / param1Steps) * (param1End - param1Start)
#     print("Solving Modes at " + param1name + " = " + str(param1Value))
#     fimmap.AddCmd(varParam1 + ".setvariable(" + param1name + "," + str(param1Value) + ")")
#     fimmap.Exec(dev + ".evlist.update()")
#     fimmap.AddCmd(dev + ".evlist.list[1].modedata.update(1)")
#     disp = fimmap.Exec(dev + ".evlist.list[1].modedata.dispersion()")
#     f.write(str(param1Value) + " ," + str(disp) + "\n")
#
# print("All done!")

#####################################################################################################################
# Variation of step index example, not all parameters (central layer dopant and thickness) TRIANGULAR
# Calculation of dispersion vs combination -> central layer dopant and thickness

varParam1 = "app.subnodes[1].subnodes[5]"  # module with variables
param1name = 'refractive index'
num1layers = 100
param1Start = 1.46
param1End = 1.47
param1Steps = 10

varParam2 = "app.subnodes[1].subnodes[5]"
param2name = "a2"  # thickness
param2Start = 2
param2End = 6
param2Steps = 16

print("Scanning " + param1name + " and " + param2name + " and extracting dispersion, group index and effective index")

# module under test
dev = "app.subnodes[1].subnodes[4]"
# object is created
fiber_profile = FiberProfile()

# first loop for changing the refractive index
for param1 in range(0, param1Steps + 1, 1):
    param1Value = param1Start + (float(param1) / param1Steps) * (param1End - param1Start)
    print("Solving Modes at " + param1name + " = " + str(param1Value) + " and")
    dop_perc_GeO2_SiO2 = fiber_profile.graded_index_profile(4, 1,param1Value, 1.45, num1layers)

    # loop to modify every layer
    for numlayer in range(0, num1layers, 1):
        fimmap.AddCmd(dev + ".layers[" + str(numlayer) + "].mx=" + str(dop_perc_GeO2_SiO2[numlayer]))

    for param2 in range(0, param2Steps + 1, 1):
        param2Value = param2Start + (float(param2) / param2Steps) * (param2End - param2Start)
        print("    " + param2name + " = " + str(param2Value))
        fimmap.AddCmd(varParam2 + ".setvariable(" + param2name + "," + str(param2Value) + ")")
        fimmap.Exec(dev + ".evlist.update(1)")
        neff = fimmap.Exec(dev + ".evlist.list[1].neff()")
        fimmap.AddCmd(dev + ".evlist.list[1].modedata.update(1)")
        GRidx = fimmap.Exec(dev + ".evlist.list[1].modedata.neffg()")
        disp = fimmap.Exec(dev + ".evlist.list[1].modedata.dispersion()")
        f.write(
            str(param1Value) + " ," + str(param2Value) + " ," + str(disp) + " ," + str(GRidx) + "," + str(neff) + "\n")

print("All done!")


# Variation of step index example, not all parameters (central layer dopant and thickness) Graded
# Calculation of dispersion vs combination -> central layer dopant and thickness

# varParam1 = "app.subnodes[1].subnodes[5]"  # module with variables
# param1name = 'refractive index'
# num1layers = 100
# param1Start = 1.46
# param1End = 1.47
# param1Steps = 2
# alpha = 2.2
#
# varParam2 = "app.subnodes[1].subnodes[5]"
# param2name = "a2"  # thickness
# param2Start = 2
# param2End = 6
# param2Steps = 16
#
# print("Scanning " + param1name + " and " + param2name + " and extracting dispersion, group index and effective index")
#
# # module under test
# dev = "app.subnodes[1].subnodes[3]"
# # object is created
# fiber_profile = FiberProfile()
#
# # first loop for changing the refractive index
# for param1 in range(0, param1Steps + 1, 1):
#     param1Value = param1Start + (float(param1) / param1Steps) * (param1End - param1Start)
#     print("Solving Modes at " + param1name + " = " + str(param1Value) + " and")
#     dop_perc_GeO2_SiO2 = fiber_profile.graded_index_profile(4, alpha,param1Value, 1.45, num1layers)
#
#     x = np.arange(0,num1layers,1)
#     plt.plot(x, dop_perc_GeO2_SiO2)
#     plt.xlabel('x')
#     plt.ylabel('y')
#     plt.title('Graded index fiber')
#
#     # loop to modify every layer
#     for numlayer in range(0, num1layers, 1):
#         fimmap.AddCmd(dev + ".layers[" + str(numlayer) + "].mx=" + str(dop_perc_GeO2_SiO2[numlayer]))
#
#     for param2 in range(0, param2Steps + 1, 1):
#         param2Value = param2Start + (float(param2) / param2Steps) * (param2End - param2Start)
#         print("    " + param2name + " = " + str(param2Value))
#         fimmap.AddCmd(varParam2 + ".setvariable(" + param2name + "," + str(param2Value) + ")")
#         fimmap.Exec(dev + ".evlist.update(1)")
#         neff = fimmap.Exec(dev + ".evlist.list[1].neff()")
#         fimmap.AddCmd(dev + ".evlist.list[1].modedata.update(1)")
#         GRidx = fimmap.Exec(dev + ".evlist.list[1].modedata.neffg()")
#         disp = fimmap.Exec(dev + ".evlist.list[1].modedata.dispersion()")
#         f.write(
#             str(param1Value) + " ," + str(param2Value) + " ," + str(disp) + " ," + str(GRidx) + "," + str(neff) + "\n")
#
# print("All done!")
# plt.show()


# TESTING CLASS FiberProfile.py

# varParam1 = "app.subnodes[1].subnodes[5]"  # module with variables
# param1name = 'refractive index'
# num1layers = 100
# param1Start = 1.46
# param1End = 1.47
# param1Steps = 2
# alpha = 2.2
#
# varParam2 = "app.subnodes[1].subnodes[5]"
# param2name = "a2"  # thickness
# param2Start = 2
# param2End = 6
# param2Steps = 16
# data = dict()
#
# print("Scanning " + param1name + " and " + param2name + " and extracting dispersion, group index and effective index")
#
# # module under test
# dev = "app.subnodes[1].subnodes[3]"
# # object is created
# fiber_profile = FiberProfile(fimmap)
#
# # first loop for changing the refractive index
# for param1 in range(0, param1Steps + 1, 1):
#     param1Value = param1Start + (float(param1) / param1Steps) * (param1End - param1Start)
#     print("Solving Modes at " + param1name + " = " + str(param1Value) + " and")
#     dop_perc_GeO2_SiO2 = fiber_profile.graded_index_profile(4, param1Value, 1.45,alpha, num1layers)
#
#     x = np.arange(0, num1layers, 1)
#     plt.plot(x, dop_perc_GeO2_SiO2)
#     plt.xlabel('x')
#     plt.ylabel('y')
#     plt.title('Graded index fiber')
#
#     # loop to modify every layer
#     for numlayer in range(0, num1layers, 1):
#         fimmap.AddCmd(dev + ".layers[" + str(numlayer) + "].mx=" + str(dop_perc_GeO2_SiO2[numlayer]))
#
#     for param2 in range(0, param2Steps + 1, 1):
#         param2Value = param2Start + (float(param2) / param2Steps) * (param2End - param2Start)
#         print("    " + param2name + " = " + str(param2Value))
#         fimmap.AddCmd(varParam2 + ".setvariable(" + param2name + "," + str(param2Value) + ")")
#         data = fiber_profile.mode_data(fimmap, dev, 1, 1, 1, 1, 1, 1, 1, '1')
#         print(data)
#
# print("All done!")
# plt.show()

f.close()
del fimmap
