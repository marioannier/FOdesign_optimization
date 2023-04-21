# Dispersion calculator
# base on DispersionCalculator.py

# from pdPythonLib import *
import fimmwavelib as fimm
from pdPythonLib import *
from math import *

##f = pdApp()
app = fimm.start_fimmwave('C:\\Program Files\\PhotonD\\Fimmwave\\bin64\\fimmwave.exe', 5101)
app.openproject(
    'D:\\OneDrive UPV\\OneDrive - UPV\\PhD-m\\2022-2023\\lines\\Nonuniformly Spaced Photonic Microwave\\Simulations_run\\FIMMWAVE_Python\\FOdesign_optimization\\Experiment_fibers.prj',
    "")

wg = app.getsubnode("subnodes[1].subnodes[1]")

setWavelengthVariable = False  # set this to true if the wavelength is set using a variable
wavelength_variable_name = "Wavelength"  # name of variable defining the wavelength
var = app.getsubnode(
    "subnodes[1].subnodes[1]")  # location of the variables node where the variable defining the wavelength is located
# also test with var = app.subnodes[1].subnodes[1]

factor = 0.002  # dispersion calculated based on data at wavelength, wavelength*(1+/-factor); recommended value: 1e-3


# dispersion versus wavelength

def CalcDispersion(wav, verbose=True, enablePolishing=False):
    beta0 = 0
    TE0 = 0
    betaMin = 0
    TEMin = 0
    betaMax = 0
    TEMax = 0
    if verbose == True:
        print("wavelength: beta, TEfrac")

    dwav = factor * wav
    wg.evlist.svp.lambda_ = wav

    if setWavelengthVariable == True:
        wg.setvariable(wavelength_variable_name, wav)

    wg.evlist.unalloc()  # unalloc() {-} delete all evs
    attemptBuildList(wg, wav)

    beta0 = wg.evlist.list[1].beta()
    TE0 = wg.evlist.list[1].modedata.tefrac
    beta0 = beta0.real
    wg.evlist.svp.lambda_ = wav + dwav

    if setWavelengthVariable == True:
        var.setvariable(wavelength_variable_name, wav + dwav)

    if enablePolishing == True:
        wg.evlist.polishevs()
    else:
        wg.evlist.unalloc()
        attemptBuildList(wg, wav + dwav)

    betaMax = wg.evlist.list[1].beta()
    TEMax = wg.evlist.list[1].modedata.tefrac
    betaMax = betaMax.real
    wg.evlist.svp.lambda_ = wav - dwav

    if setWavelengthVariable == True:
        var.setvariable(wavelength_variable_name, wav - dwav)
    if enablePolishing == True:
        wg.evlist.polishevs()
    else:
        wg.evlist.unalloc()
        attemptBuildList(wg, wav - dwav)

    betaMin = wg.evlist.list[1].beta()
    TEMin = wg.evlist.list[1].modedata.tefrac
    betaMin = betaMin.real
    if verbose == True:
        print(str(wav - dwav) + ": " + str(betaMin) + ", " + str(TEMin))
        print(str(wav) + ": " + str(beta0) + ", " + str(TE0))
        print(str(wav + dwav) + ": " + str(betaMax) + ", " + str(TEMax))
    return -1 / (2 * pi * 3e8 * 1e-12) / dwav ** 2 * (
            (wav + dwav / 2) ** 2 * (betaMax - beta0) - (wav - dwav / 2) ** 2 * (beta0 - betaMin))

def attemptBuildList(wg, wav):
    found = 0
    idxfound = 0
    while found == 0:
        idxfound = idxfound + 1
        error = wg.evlist.update()
        try:
            if error[:5] == "ERROR":  # problem in calculating mode list; can happen in rare occasions with FMM Solver
                wg.evlist.svp.lambda_ = wav + idxfound * 1e-7
            else:
                found = 1
        except TypeError:
            found = 1

print("wavelength, dispersion")

Nsteps = 50
wavmin = 1.2
wavmax = 1.6

for i in range(0, Nsteps, 1):
    wav = wavmin + float(i) / (Nsteps - 1) * (wavmax - wavmin)
    disCalc = CalcDispersion(wav, verbose=False, enablePolishing=False)
    print(str(wav) + ", " + str(disCalc))

print("All done!")

fimm.disconnect_fimmwave()
