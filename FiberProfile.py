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

    def graded_index_profile(self, a1, n1, n2, alpha, steps):
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

    def mode_data(self, fimmap, dev, beta, neff, a_eff, alpha, dispersion, isLeaky, neffg, mode='1'):

        data = {'beta': 0, 'neff': 0, 'a_eff': 0, 'alpha': 0, 'dispersion': 0, 'isLeaky': 0, 'neffg': 0}

        fimmap.Exec(dev + ".evlist.update(1)")
        if beta == 1:
            data['beta'] = fimmap.Exec(dev + ".evlist.list[" + mode + "].beta()")
        if neff == 1:
            data['neef'] = fimmap.Exec(dev + ".evlist.list[" + mode + "].neff()")

        fimmap.AddCmd(dev + ".evlist.list[" + mode + "].modedata.update(1)")
        if a_eff == 1:
            data['a_eff'] = fimmap.Exec(dev + ".evlist.list[" + mode + "].modedata.a_eff()")
        if alpha == 1:
            data['alpha'] = fimmap.Exec(dev + ".evlist.list[" + mode + "].modedata.alpha()")
        if dispersion == 1:
            data['dispersion'] = fimmap.Exec(dev + ".evlist.list[" + mode + "].modedata.dispersion()")
        if isLeaky == 1:
            data['isLeaky'] = fimmap.Exec(dev + ".evlist.list[" + mode + "].modedata.isLeaky()")
        if neffg == 1:
            data['neffg'] = fimmap.Exec(dev + ".evlist.list[" + mode + "].modedata.neffg()")

        return data

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

    def builder_profile(self, dev, n1, n2, n3, n4, a1, a2, a3, a4, pro_type, alpha):
        refrac_index = [n1, n2, n3, n4]
        sizes = [a1, a2, a3, a4]
        # dopant percent of SiO2
        SiO2_perct = 0.05
        F_SiO2_1 = 0

        match pro_type:
            case "Step Index":
                n_steps = 1
                # creating layers
                self.fimmap.Exec(dev + ".insertlayer(3)")
                self.fimmap.Exec(dev + ".insertlayer(4)")
                # create a variable
                # self.fimmap.Exec('app.subnodes[1].addsubnode(pdVariablesNode,"Variables 1")')
                # self.fimmap.Exec('app.subnodes[1].subnodes[4].addvariable(n2)')
                # self.fimmap.Exec('app.subnodes[1].subnodes[4].setvariable(n2,"0.05")')
                # setting materials
                self.fimmap.Exec(dev + '.layers[1].setMAT(GeO2-SiO2)')
                self.fimmap.Exec(dev + '.layers[2].setMAT(SiO2)')
                self.fimmap.Exec(dev + '.layers[3].setMAT(F-SiO2_1)')
                self.fimmap.Exec(dev + '.layers[4].setMAT(SiO2)')

                # until the moment n2=n4 -> no se como obtener el indice de refraccion a partir de la data base
                # CONFLICT ->  I change intentionally the order of n1 & n2 to obtain the correct result
                dop_perct = self.graded_index_profile(a1, n2, n1, alpha, n_steps)
                dop_perct = np.append(dop_perct, [SiO2_perct, F_SiO2_1, SiO2_perct])
                print(dop_perct)

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
                dop_perct = self.graded_index_profile(a1, n1, n2, alpha, n_steps)

                # plotting to check
                x = np.arange(0, self.a1, self.a1 / self.steps)
                plt.plot(x, dop_perct)
                plt.show()

                dop_perct = np.append(dop_perct, [SiO2_perct, F_SiO2_1, SiO2_perct])

                # loop to modify every layer
                for numlayer in range(1, n_steps + 3, 1):
                    if numlayer < n_steps:
                        self.fimmap.Exec(dev + ".insertlayer(" + str(numlayer) + ")")
                        self.fimmap.Exec(dev + '.layers[' + str(numlayer) + '].size=' + str(sizes[0]/n_steps))
                        self.fimmap.Exec(dev + ".layers[" + str(numlayer) + "].setMAT(GeO2-SiO2)")
                        self.fimmap.Exec(dev + ".layers[" + str(numlayer) + "].mx=" + str(dop_perct[numlayer - 1]))
                    else:
                        self.fimmap.Exec(dev + '.layers[' + str(numlayer) + '].size=' + str(sizes[numlayer - n_steps]))

            case _:
                raise EnvironmentError("type not specify or incorrect")
