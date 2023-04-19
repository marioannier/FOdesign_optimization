from pdPythonLib import *

fimmap = pdApp()
fimmap.ConnectToApp("localhost", 5101)

f = open('D_C7.csv', 'w')

varParam1 = "app.subnodes[1].subnodes[2]"
param1name = "lambda"
param1Start = 1.4
param1End = 1.9
param1Steps = 50

print("Scanning " + param1name + " and extracting the propagation constant")

dev = "app.subnodes[1].subnodes[1]"

for param1 in range(0, param1Steps + 1, 1):
    param1Value = param1Start + (float(param1) / param1Steps) * (param1End - param1Start)
    print("Solving Modes at " + param1name + " = " + str(param1Value))
    fimmap.AddCmd(varParam1 + ".setvariable(" + param1name + "," + str(param1Value) + ")")
    fimmap.Exec(dev + ".evlist.update()")
    fimmap.AddCmd(dev + ".evlist.list[1].modedata.update(1)")
    disp = fimmap.Exec(dev + ".evlist.list[1].modedata.dispersion()")
    f.write(str(param1Value) + " ," + str(disp) + "\n")

print("All done!")

f.close()
del fimmap


