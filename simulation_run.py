import os
import numpy as np
import fiber_profile_gen as fp


class SimulationRun:
    def __init__(self, fimmap=object):
        self.fimmap = fimmap

    def solver_config(self, solver='FDM Fiber Solver'):

        dev = 'app.subnodes[1].subnodes[1]'  # the device is one because I am going to have only one core type per project

        match solver:
            case 'FDM Fiber Solver':
                self.fimmap.Exec(dev + ".evlist.svp.hcurv=0")
                self.fimmap.Exec(dev + ".evlist.svp.solvid=192")
                self.fimmap.Exec(dev + ".evlist.svp.hsymmetry=0")
                self.fimmap.Exec(dev + ".evlist.svp.vsymmetry=0")
                self.fimmap.Exec(dev + ".evlist.svp.buff=V1 1000 0 10 1 2")
                self.fimmap.Exec(dev + ".evlist.mlp.autorun=1")
                self.fimmap.Exec(dev + ".evlist.mlp.speed=0")
                self.fimmap.Exec(dev + ".evlist.mlp.mintefrac=0")
                self.fimmap.Exec(dev + ".evlist.mlp.maxtefrac=100")
                self.fimmap.Exec(dev + ".evlist.mlp.maxnmodes=10")
                self.fimmap.Exec(dev + ".evlist.mlp.evstart=1e+50")
                self.fimmap.Exec(dev + ".evlist.mlp.evend=-1e+50")
                self.fimmap.Exec(dev + ".evlist.mlp.nx=120")
                self.fimmap.Exec(dev + ".evlist.mlp.ny=120")

            case 'GFS Fiber Solver':
                self.fimmap.Exec(dev + ".evlist.svp.lambda=1.55")
                self.fimmap.Exec(dev + ".evlist.svp.hcurv=0")
                self.fimmap.Exec(dev + ".evlist.svp.solvid=68")
                self.fimmap.Exec(dev + ".evlist.svp.hsymmetry=0")
                self.fimmap.Exec(dev + ".evlist.svp.vsymmetry=0")
                self.fimmap.Exec(dev + ".evlist.svp.buff=V1 0 10 1 2")
                self.fimmap.Exec(dev + ".evlist.mlp.autorun=1")
                self.fimmap.Exec(dev + ".evlist.mlp.speed=0")
                self.fimmap.Exec(dev + ".evlist.mlp.mintefrac=0")
                self.fimmap.Exec(dev + ".evlist.mlp.maxtefrac=100")
                self.fimmap.Exec(dev + ".evlist.mlp.maxnmodes=10")
                self.fimmap.Exec(dev + ".evlist.mlp.evstart=1e+50")
                self.fimmap.Exec(dev + ".evlist.mlp.evend=-1e+50")
                self.fimmap.Exec(dev + ".evlist.mlp.nx=120")
                self.fimmap.Exec(dev + ".evlist.mlp.ny=120")

            case _:
                raise EnvironmentError("type of solver is not specify or is incorrect")

    import numpy as np

    def simulate(self, param_Scan={"beta": True, "neff": True, "a_eff": True, "alpha": True, "dispersion": True,
                                   "isLeaky": True, "neffg": True, "fillFac": True, "gammaE": True}, mode='1'):
        dev = 'app.subnodes[1].subnodes[1]'  # the device is one because I am going to have only one core type per project

        num_true_values = list(param_Scan.values()).count(True)  # determine the length of the parameters to save

        data = np.zeros(num_true_values)

        self.fimmap.Exec(dev + ".evlist.update(1)")

        def get_valid_number(value):
            try:
                return float(value)
            except (ValueError, TypeError):
                return -1000

        if param_Scan['beta']:
            data[0] = get_valid_number(np.real(self.fimmap.Exec(dev + ".evlist.list[" + mode + "].beta()")))
        if param_Scan['neff']:
            data[1] = get_valid_number(np.real(self.fimmap.Exec(dev + ".evlist.list[" + mode + "].neff()")))
        self.fimmap.AddCmd(dev + ".evlist.list[" + mode + "].modedata.update(1)")
        if param_Scan['a_eff']:
            data[2] = get_valid_number(self.fimmap.Exec(dev + ".evlist.list[" + mode + "].modedata.a_eff()"))
        if param_Scan['alpha']:
            data[3] = get_valid_number(self.fimmap.Exec(dev + ".evlist.list[" + mode + "].modedata.alpha()"))
        if param_Scan['dispersion']:
            data[4] = get_valid_number(self.fimmap.Exec(dev + ".evlist.list[" + mode + "].modedata.dispersion()"))
        if param_Scan['isLeaky']:
            data[5] = get_valid_number(self.fimmap.Exec(dev + ".evlist.list[" + mode + "].modedata.isLeaky()"))
        if param_Scan['neffg']:
            data[6] = get_valid_number(self.fimmap.Exec(dev + ".evlist.list[" + mode + "].modedata.neffg()"))
        if param_Scan['fillFac']:
            data[7] = get_valid_number(self.fimmap.Exec(dev + ".evlist.list[" + mode + "].modedata.fillFac()"))
        if param_Scan['gammaE']:
            data[8] = get_valid_number(self.fimmap.Exec(dev + ".evlist.list[" + mode + "].modedata.gammaE()"))

        return data
