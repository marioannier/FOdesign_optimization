# Quiero que esta clase reciba como entrada los diferente parametros n1, n2, n3, n4, a1, a2, a3, a4 del perfil
# que ademas reciba el tipo de perfil: step, triangular o graded, cada una puede ser una function y recibir los
# parametros que necesita como alpha y que a su vez me cree una FWG con la carateriaticas deseadas

from pdPythonLib import *
import numpy as np
import matplotlib.pyplot as plt
import array


class FiberProfile:
    def __init__(self, fimmap=object):
        # by default it generate a triangular a=1
        self.fimmap = fimmap

    def __set__(self, fimmap=object):
        self.fimmap = fimmap

    def graded_refindex_gene(self, a1, n1, n2, alpha, steps):
        self.a1 = a1
        self.n1 = n1
        self.n2 = n2
        self.alpha = alpha
        self.steps = steps
        x = np.arange(0, self.a1, self.a1 / self.steps)
        y = np.zeros(self.steps)

        A = np.zeros((self.steps, 1))
        B = A.astype('str')

        g = self.a1 / self.steps

        for j in range(self.steps):
            y[j] = (6.67677 * self.n1 * (1 - 2 * ((self.n1 ** 2 - self.n2 ** 2) / (2 * self.n1 ** 2)) * (
                    x[j] / self.a1) ** self.alpha) ** (
                            1 / 2) - 9.64142)  # porcentaje j
            B[j] = y[j]
        return y
        # np.savetxt('dop_perc_GeO2-SiO2.txt', B, delimiter='\t', fmt='%s')
        # with open('dop_perc_GeO2-SiO2.txt') as f:
        #    print(f.read())

        # plt.plot(x, y)
        # plt.xlabel('radius')
        # plt.ylabel('dop_perc_GeO2-SiO2')
        # plt.title('Graded index fiber')
        # plt.show()

    def graded_dopa_gene(self, alpha, dopa_max, steps):
        # dopa_max in number NOT percentage

        m = -dopa_max / (steps ** alpha)
        y = np.zeros(steps)

        for j in range(steps):
            y[j] = (m * (j ** alpha) + dopa_max)

        return y

    def add_project(self, name='fiber_test', dir='nodir'):
        self.fimmap.Exec('app.addsubnode(' + name + 'fimmwave_prj, "project_test")')
        if dir == 'nodir':
            raise EnvironmentError("Ivalid or not selected Directory")
        else:
            self.fimmap.Exec('app.subnodes[1].savetofile(' + dir + ')')

    def add_moduleFWG(self, type, data_base='refbase.mat'):
        match type:
            case "Step Index":
                name = 'step_index'
                self.fimmap.Exec('app.subnodes[1].addsubnode(fwguideNode,' + name + ')')
                self.fimmap.Exec('app.subnodes[1].subnodes[1].setmaterbase("' + data_base + '")')

            case "Triangular":
                name = 'triangular'
                self.fimmap.Exec('app.subnodes[1].addsubnode(fwguideNode,' + name + ')')
                self.fimmap.Exec('app.subnodes[1].subnodes[2].setmaterbase("' + data_base + '")')

            case "Graded":
                name = 'graded'
                self.fimmap.Exec('app.subnodes[1].addsubnode(fwguideNode,' + name + ')')
                self.fimmap.Exec('app.subnodes[1].subnodes[3].setmaterbase("' + data_base + '")')
            case _:
                raise EnvironmentError("type not specify or incorrect")

    def builder_profile(self, dev, n1_dop, n2_dop, n3_dop, n4_dop, a1, a2, a3, a4, pro_type, alpha):
        dop_perct = [n1_dop, n2_dop, n3_dop, n4_dop]
        sizes = [a1, a2, a3, a4]
        # dopant percent of SiO2
        a1_material = 'GeO2-SiO2'
        a2_material = 'SiO2'
        a3_material = 'F-SiO2_1'
        a4_material = 'SiO2'

        match pro_type:
            case "Step Index":
                # creating layers
                self.fimmap.Exec(dev + ".insertlayer(3)")
                self.fimmap.Exec(dev + ".insertlayer(4)")
                # setting materials
                self.fimmap.Exec(dev + '.layers[1].setMAT(' + a1_material + ')')
                self.fimmap.Exec(dev + '.layers[2].setMAT(' + a2_material + ')')
                self.fimmap.Exec(dev + '.layers[3].setMAT(' + a3_material + ')')
                self.fimmap.Exec(dev + '.layers[4].setMAT(' + a4_material + ')')

                # modifying layer parameters (sizes) & setting dopant percentage
                for numlayer in range(1, 5, 1):
                    self.fimmap.Exec(dev + '.layers[' + str(numlayer) + '].size=' + str(sizes[numlayer - 1]))
                    self.fimmap.Exec(dev + '.layers[' + str(numlayer) + '].mx=' + str(dop_perct[numlayer - 1]))

            case "Graded":
                n_steps = 100
                # creating layers
                self.fimmap.Exec(dev + ".insertlayer(3)")
                # setting materials I don't set the matrerial for layer 1 'cause is modify later
                self.fimmap.Exec(dev + '.layers[1].setMAT(SiO2)')
                self.fimmap.Exec(dev + '.layers[2].setMAT(F-SiO2_1)')
                self.fimmap.Exec(dev + '.layers[3].setMAT(SiO2)')
                dop_perct_grad = self.graded_dopa_gene(alpha, n1_dop, n_steps)

                # plotting to check
                x = np.arange(0, a1, a1 / n_steps)
                plt.plot(x, dop_perct_grad)
                plt.show()

                dop_perct.pop(0)
                dop_perct = np.append(dop_perct_grad, dop_perct)

                # loop to modify every layer
                for numlayer in range(1, n_steps + 3, 1):
                    if numlayer < n_steps:
                        self.fimmap.Exec(dev + ".insertlayer(" + str(numlayer) + ")")
                        self.fimmap.Exec(dev + '.layers[' + str(numlayer) + '].size=' + str(sizes[0] / n_steps))
                        self.fimmap.Exec(dev + ".layers[" + str(numlayer) + "].setMAT(GeO2-SiO2)")
                        self.fimmap.Exec(dev + ".layers[" + str(numlayer) + "].mx=" + str(dop_perct[numlayer - 1]))
                    else:
                        self.fimmap.Exec(dev + '.layers[' + str(numlayer) + '].size=' + str(sizes[numlayer - n_steps]))
                        self.fimmap.Exec(dev + '.layers[' + str(numlayer) + '].mx=' + str(dop_perct[numlayer]))

            case _:
                raise EnvironmentError("type not specify or incorrect")

    def update_profile(self, dev, n1_dop, n2_dop, n3_dop, n4_dop, a1, a2, a3, a4, pro_type, alpha):
        dop_perct = [n1_dop, n2_dop, n3_dop, n4_dop]
        sizes = [a1, a2, a3, a4]
        # dopant percent of SiO2
        a1_material = 'GeO2-SiO2'
        a2_material = 'SiO2'
        a3_material = 'F-SiO2_1'
        a4_material = 'SiO2'
        match pro_type:
            case "Step Index":

                # setting materials -> COMMENTED 'CAUSE WAS ALREADY SETTES
                # self.fimmap.Exec(dev + '.layers[1].setMAT(' + a1_material + ')')
                # self.fimmap.Exec(dev + '.layers[2].setMAT(' + a2_material + ')')
                # self.fimmap.Exec(dev + '.layers[3].setMAT(' + a3_material + ')')
                # self.fimmap.Exec(dev + '.layers[4].setMAT(' + a4_material + ')')

                # modifying layer parameters (sizes) & setting dopant percentage
                for numlayer in range(1, 5, 1):
                    self.fimmap.Exec(dev + '.layers[' + str(numlayer) + '].size=' + str(sizes[numlayer - 1]))
                    self.fimmap.Exec(dev + '.layers[' + str(numlayer) + '].mx=' + str(dop_perct[numlayer - 1]))

            case "Graded":
                n_steps = 100
                dop_perct_grad = self.graded_dopa_gene(alpha, n1_dop, n_steps)
                dop_perct.pop(0)
                dop_perct = np.append(dop_perct_grad, dop_perct)

                # plotting to check -> CHANGE TO PLOT DIFFERENT PARAMETERS THE PREVIOUS ONES AND THE FORMER
                # x = np.arange(0, a1, a1 / n_steps)
                # plt.plot(x, dop_perct_grad)
                # plt.show()

                # loop to modify every layer
                for numlayer in range(1, n_steps + 3, 1):
                    if numlayer < n_steps:
                        self.fimmap.Exec(dev + '.layers[' + str(numlayer) + '].size=' + str(sizes[0] / n_steps))
                        self.fimmap.Exec(dev + ".layers[" + str(numlayer) + "].mx=" + str(dop_perct[numlayer - 1]))
                    else:
                        self.fimmap.Exec(dev + '.layers[' + str(numlayer) + '].size=' + str(sizes[numlayer - n_steps]))
                        self.fimmap.Exec(dev + '.layers[' + str(numlayer) + '].mx=' + str(dop_perct[numlayer]))

            case _:
                raise EnvironmentError("type not specify or incorrect")

    def mode_data(self, dev, param_Scan=None, mode='1'):

        if param_Scan is None:
            param_Scan = {"beta": False, "neff": False, "a_eff": False, "alpha": False, "dispersion": True,
                          "isLeaky": False, "neffg": False}
        data = np.zeros(7)

        self.fimmap.Exec(dev + ".evlist.update(1)")
        if param_Scan['beta']:
            data[0] = self.fimmap.Exec(dev + ".evlist.list[" + mode + "].beta()")
        if param_Scan['neff']:
            data[1] = self.fimmap.Exec(dev + ".evlist.list[" + mode + "].neff()")
        self.fimmap.AddCmd(dev + ".evlist.list[" + mode + "].modedata.update(1)")
        if param_Scan['a_eff']:
            data[2] = self.fimmap.Exec(dev + ".evlist.list[" + mode + "].modedata.a_eff()")
        if param_Scan['alpha']:
            data[3] = self.fimmap.Exec(dev + ".evlist.list[" + mode + "].modedata.alpha()")
        if param_Scan['dispersion']:
            data[4] = self.fimmap.Exec(dev + ".evlist.list[" + mode + "].modedata.dispersion()")
        if param_Scan['isLeaky']:
            data[5] = self.fimmap.Exec(dev + ".evlist.list[" + mode + "].modedata.isLeaky()")
        if param_Scan['neffg']:
            data[6] = self.fimmap.Exec(dev + ".evlist.list[" + mode + "].modedata.neffg()")

        return data

    def scan_lambda(self, dev, lambda_s, lambda_e, steps, param_Scan=None):

        if param_Scan is None:
            param_Scan = {"beta": False, "neff": False, "a_eff": False, "alpha": False, "dispersion": True,
                          "isLeaky": False, "neffg": False}

        data_scan = np.zeros((steps, 8))
        data_scan = data_scan.astype('str')

        print("Scanning lambda and extracting: " + ", ".join(param_Scan))

        for i in range(0, steps, 1):
            lx = lambda_s + (float(i) / steps) * (lambda_e - lambda_s)
            print("Solving Modes at " + str(lx))
            self.fimmap.Exec(dev + ".evlist.svp.lambda=" + str(lx))
            data_scan[i + 1, :] = list(self.mode_data(dev, param_Scan))
            data_scan[i, 0] = str(lx)

        return data_scan
