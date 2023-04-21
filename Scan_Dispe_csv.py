from pdPythonLib import *
import fimmwavelib as fimm

fimmap = pdApp()
fimmap.StartApp('C:\\Program Files\\PhotonD\\Fimmwave\\bin64\\fimmwave.exe', 5101)
dir ='(D:\\OneDrive UPV\\OneDrive - UPV\\PhD-m\\2022-2023\\lines\\Nonuniformly Spaced Photonic Microwave\\Simulations_run\\FIMMWAVE_Python\\FOdesign_optimization\\Experiment_fibers.prj,"")';
fimmap.Exec("app.openproject"+dir)

# fimmap.ConnectToApp("localhost")

#f = open('D_C7.csv', 'w')

varParam1 = "app.subnodes[1].subnodes[5]" # module with variables
param1name = "lambda"
param1Start = 1.4
param1End = 1.9
param1Steps = 50

print("Scanning " + param1name + " and extracting the propagation constant")

dev = "app.subnodes[1].subnodes[2]" # module under test

for param1 in range(0, param1Steps + 1, 1):
    param1Value = param1Start + (float(param1) / param1Steps) * (param1End - param1Start)
    print("Solving Modes at " + param1name + " = " + str(param1Value))
    fimmap.AddCmd(varParam1 + ".setvariable(" + param1name + "," + str(param1Value) + ")")
    fimmap.Exec(dev + ".evlist.update()")
    fimmap.AddCmd(dev + ".evlist.list[1].modedata.update(1)")
    disp = fimmap.Exec(dev + ".evlist.list[1].modedata.dispersion()")
    #f.write(str(param1Value) + " ," + str(disp) + "\n")

print("All done!")
#f.close()

#f = open('Disp-ng-neff_Scan_n1_a2.csv', 'w')

varParam1 = "app.subnodes[1].subnodes[5]"
param1name = "n1" # core dopant
param1Start = 0.08
param1End = 0.09
param1Steps = 10

varParam2 = "app.subnodes[1].subnodes[5]"
param2name = "a2" #thickness
param2Start = 2
param2End = 6
param2Steps = 16

print("Scanning " + param1name + " and " + param2name + " and extracting dispersion, group index and effective index")


dev = "app.subnodes[1].subnodes[2]"

for param1 in range(0, param1Steps + 1, 1):
    param1Value = param1Start + (float(param1) / param1Steps) * (param1End - param1Start)
    print("Solving Modes at " + param1name + " = " + str(param1Value) + " and")
    fimmap.AddCmd(varParam1 + ".setvariable(" + param1name + "," + str(param1Value) + ")")
    for param2 in range(0, param2Steps + 1, 1):
        param2Value = param2Start + (float(param2) / param2Steps) * (param2End - param2Start)
        print("    " + param2name + " = " + str(param2Value))
        fimmap.AddCmd(varParam2 + ".setvariable(" + param2name + "," + str(param2Value) + ")")
        fimmap.Exec(dev + ".evlist.update")
        neff = fimmap.Exec(dev + ".evlist.list[1].neff")
        fimmap.AddCmd(dev + ".evlist.list[1].modedata.update(1)")
        GRidx = fimmap.Exec(dev + ".evlist.list[1].modedata.neffg")
        disp = fimmap.Exec(dev + ".evlist.list[1].modedata.dispersion")
        # f.write(
        #     str(param1Value) + " ," + str(param2Value) + " ," + str(disp) + " ," + str(GRidx) + "," + str(neff) + "\n")

print("All done!")

#f.close()
del fimmap


