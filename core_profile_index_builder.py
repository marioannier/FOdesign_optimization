import os
import numpy as np
import fiber_profile_gen as fp



class ProfileIndexBuilder:
    def __init__(self, fimmap=object):
        # by default it generate a triangular a=1
        self.fimmap = fimmap

    def create_fimm_project(self, name='Fimmwave Project 1', direc=os.getcwd()):
        if not os.path.exists(direc):
            raise FileNotFoundError(f"Directory '{direc}' does not exist.")

        self.fimmap.Exec('app.addsubnode(fimmwave_prj,' + name + ')')
        self.fimmap.Exec('app.subnodes[1].savetofile(' + direc + ')')

    def add_moduleFWG(self, name='FWG Waveguide 1', data_base='refbase.mat'):
        self.fimmap.Exec('app.subnodes[1].addsubnode(fwguideNode,' + name + ')')
        self.fimmap.Exec('app.subnodes[1].subnodes[1].setmaterbase("' + data_base + '")')

    def builder_profile(self, dev, sizes, dop_perct, profile_type, materials, alpha):
        n_steps = 100

        for i, type_regions in enumerate(profile_type):

            # creating the extra layers
            num_layers = self.obtain_num_layer(dev)
            if i > int(num_layers)-1:
                self.fimmap.Exec(dev + ".insertlayer(" + str(i+1) + ")")

            # creating the non-constant layers
            if type_regions != 'contant':
                match type_regions:
                    case "Linear":
                        dop_perct_grad = fp.FiberProfileGen.graded_refindex(self, alpha, dop_perct[i], n_steps)

                    case "Graded":
                         dop_perct_grad = fp.FiberProfileGen.graded_refindex(self, alpha, dop_perct[i], n_steps)

                    case "Raised cosine":
                        dop_perct_grad = fp.FiberProfileGen.rc_refindex(self, alpha, dop_perct[i], n_steps)

                dop_perct.pop(0)
                dop_perct = np.append(dop_perct_grad, dop_perct)

                #### me quede




            # +1 added 'cause fimmap start at 1
            self.fimmap.Exec(dev + '.layers[' + str(i + 1) + '].setMAT(' + materials[i] + ')')
            self.fimmap.Exec(dev + '.layers[' + str(i + 1) + '].size=' + str(sizes[i]))

            # for these cases, the dopant percentage is irrelevant
            if "F-SiO2" not in materials[i]:
                self.fimmap.Exec(dev + '.layers[' + str(i + 1) + '].mx=' + str(dop_perct[i]))

            # for measuring a certain parameters only in the core
            if i == 1:
                self.fimmap.Exec(dev + '.layers[' + str(i) + '].cfseg=1')

    def obtain_num_layer(self, dev):
        # return a float with the number of layers
        num_layers = self.fimmap.Exec(dev + '.nlayers()')
        return num_layers
