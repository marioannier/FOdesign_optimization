from pdPythonLib import *
from array import *
fimm = pdApp()
fimm.ConnectToApp("localhost",5102)

f = open('Disp-ng-neff_Scan_n1_a2.csv', 'w')

varParam1 = "app.subnodes[1].subnodes[7]"
param1name = "n11"
param1Start = 0.08
param1End = 0.09
param1Steps = 10

varParam2 = "app.subnodes[1].subnodes[7]"
param2name = "a21"
param2Start = 2
param2End = 6
param2Steps = 16


print "Scanning " + param1name + " and " + param2name + " and extracting dispersion, group index and effective index"

dev = "app.subnodes[1].subnodes[9]"
    
for param1 in range(0,param1Steps+1,1):
    param1Value = param1Start+(float(param1)/param1Steps)*(param1End-param1Start)
    print "Solving Modes at " + param1name + " = " + str(param1Value) + " and"
    fimm.AddCmd(varParam1+".setvariable("+param1name+","+str(param1Value)+")")
    for param2 in range (0,param2Steps+1,1):
        param2Value = param2Start+(float(param2)/param2Steps)*(param2End-param2Start)
        print "    " + param2name + " = " + str(param2Value)
        fimm.AddCmd(varParam2+".setvariable("+param2name+","+str(param2Value)+")")
        fimm.Exec(dev+".evlist.update")
        neff = fimm.Exec(dev+".evlist.list[1].neff")
        fimm.AddCmd(dev+".evlist.list[1].modedata.update(1)")
        GRidx = fimm.Exec(dev+".evlist.list[1].modedata.neffg")
        disp = fimm.Exec(dev+".evlist.list[1].modedata.dispersion")
        f.write(str(param1Value) + " ," + str(param2Value) + " ," + str(disp) + " ," + str(GRidx) + "," + str(neff) + "\n")
  

print "All done!"

f.close
del fimm
