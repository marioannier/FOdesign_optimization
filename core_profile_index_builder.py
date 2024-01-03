import os
import numpy as np
import fiber_profile_gen as fp


class ProfileIndexBuilder:
    def __init__(self, fimmap=object):
        self.fimmap = fimmap

    def create_fimm_project(self, name='Fimmwave Project 1', direc=os.getcwd()):
        if not os.path.exists(direc):
            raise FileNotFoundError(f"Directory '{direc}' does not exist.")

        self.fimmap.Exec('app.addsubnode(fimmwave_prj,' + name + ')')
        self.fimmap.Exec('app.subnodes[1].savetofile(' + direc + ')')

    def add_moduleFWG(self, name='FWG Waveguide 1', data_base='refbase_2.mat'):
        self.fimmap.Exec('app.subnodes[1].addsubnode(fwguideNode,' + name + ')')
        self.fimmap.Exec('app.subnodes[1].subnodes[1].setmaterbase("' + data_base + '")')

    def builder_profile(self, dev, sizes, dop_perct, profile_type, materials, alpha, n_steps=100):

        # obtain the total number of layers
        num_layers = self.obtain_num_layer(dev)

        # Deleting all but first layer
        while num_layers > 1:
            self.fimmap.Exec(dev + ".deletelayer(" + str(num_layers) + ")")
            num_layers = self.obtain_num_layer(dev)

        for i, type_regions in enumerate(profile_type):
            # obtain the total number of layers
            last_layer = self.obtain_num_layer(dev)

            # creating the constant profile index layers
            if type_regions == 'Contant':
                if last_layer == 1 and i == 0:
                    # rewriting the first layer
                    current_layer = last_layer
                    self.fimmap.Exec(dev + '.layers[1].cfseg=1')  # for measuring a certain parameters only in the core
                else:
                    current_layer = last_layer + 1
                    self.fimmap.Exec(dev + '.insertlayer(' + str(current_layer) + ')')
                self.fimmap.Exec(dev + '.layers[' + str(current_layer) + '].setMAT(' + materials[i] + ')')
                self.fimmap.Exec(dev + '.layers[' + str(current_layer) + '].size=' + str(sizes[i]))

                # for these cases, the dopant percentage is irrelevant
                if "F-SiO2" not in materials[i]:
                    self.fimmap.Exec(dev + '.layers[' + str(current_layer) + '].mx=' + str(dop_perct[i]))

            # creating the non-constant layers
            else:
                if "F-SiO2" in materials[i]:
                    raise EnvironmentError("cannot be construct variable index profile with F-SiO2 at 1 or 2 %")

                match type_regions:
                    # Triangular or Graded
                    case "Linear" | "Graded":
                        dop_perct_var = self.graded_refindex(alpha[i], dop_perct[i], n_steps)

                    # Raised cosine
                    case "Raised cosine":
                        dop_perct_var = self.rc_refindex(alpha[i], dop_perct[i], n_steps)

                    case "Custome function":
                        # working on
                        pass

                # loop to modify every layer
                for numlayer in range(1, n_steps, 1):
                    current_layer = last_layer + numlayer
                    self.fimmap.Exec(dev + '.insertlayer(' + str(current_layer) + ')')
                    self.fimmap.Exec(dev + '.layers[' + str(current_layer) + '].size=' + str(sizes[i] / n_steps))
                    self.fimmap.Exec(dev + '.layers[' + str(current_layer) + '].setMAT(' + materials[i] + ')')
                    self.fimmap.Exec(dev + ".layers[" + str(current_layer) + "].mx=" + str(dop_perct_var[numlayer - 1]))
                    if last_layer == 1 and i == 0:
                        self.fimmap.Exec(dev + '.layers[' + str(current_layer) + '].cfseg=1')
                if last_layer == 1 and i == 0:
                    # eliminating the first layer, it is the default
                    self.fimmap.Exec(dev + ".deletelayer(1)")

    def obtain_num_layer(self, dev):
        # return a float with the number of layers
        num_layers = self.fimmap.Exec(dev + '.nlayers()')
        return num_layers

    def set_material_db(self, db_dir, db_name='refbase_2.mat'):
        dev = 'app.subnodes[1].subnodes[1]'  # the device is one because I am going to have only one core type per project
        data_base_data = db_dir + '\\' + db_name
        self.fimmap.Exec(dev + '.setmaterbase(' + data_base_data + ')')

    def rc_refindex(self, alpha, dopa_max, steps):
        # based on : https://doi.org/10.1016/j.yofte.2021.102777
        # Multicore raised cosine fibers for next generation space division multiplexing systems
        # refractive index relation with GiO2-SiO2 percentage Percentage = -6.67677 * refractive_index + 9.64142
        n1 = (dopa_max + 9.6495) / 6.6823
        n2 = 9.6495 / 6.6823  # zero dopant n2 = 1.4440236217

        y = np.zeros(steps)
        perc = np.zeros(steps)

        for j in range(steps):
            if j <= ((1 - alpha) * (steps / 2)):
                y[j] = n1
            elif ((1 - alpha) * (steps / 2)) < j <= ((1 + alpha) * (steps / 2)):
                y[j] = n2 + 0.5 * (n1 - n2) * (
                        1 + np.cos(np.pi / (steps * alpha) * (j - steps * 0.5 * (1 - alpha))))
            else:
                y[j] = n2

            perc[j] = 6.6823 * y[j] - 9.6495
        return perc.round(4)

    def graded_refindex(self, alpha, dopa_max, steps):
        # refractive index relation with GiO2-SiO2 percentage Percentage = -6.67677 * refractive_index + 9.64142
        n1 = (dopa_max + 9.6495) / 6.6823
        n2 = 9.6495 / 6.6823  # zero dopant n2 = 1.4440236217

        y = np.zeros(steps)
        perc = np.zeros(steps)

        delta = (n1 ** 2 - n2 ** 2) / (2 * n1 ** 2)

        for j in range(steps):
            y[j] = (n1 * np.sqrt(1 - 2 * delta * (j / steps) ** alpha))
            perc[j] = 6.6823 * y[j] - 9.6495

        return perc.round(4)


if __name__ == "__main__":
    from fiber_design import *
    from core_profile_index_builder import *

    fimmap = pdApp()
    fimmap.StartApp('C:\\Program Files\\PhotonD\\Fimmwave\\bin64\\fimmwave.exe', 5101)

    test_dir = 'D:\\OneDrive UPV\\OneDrive - UPV\PhD-m\\2023-2024\\FiberDesin_PhotonD\\FOdesign_optimization'
    fiber_profile = ProfileIndexBuilder(fimmap)
    fiber_profile.create_fimm_project('test2', test_dir)
    fiber_profile.add_moduleFWG('Module 1')

    dev = "app.subnodes[1].subnodes[1]"
    sizes = [5, 2, 3, 4, 19]
    dop_perct = [0.5, 0, 0.2, 0.8, 0]
    profile_type = ['Contant', 'Contant', 'Contant', 'Contant', 'Contant']
    materials = ['GeO2-SiO2', 'GeO2-SiO2', 'GeO2-SiO2', 'GeO2-SiO2', 'GeO2-SiO2']
    alpha = [2, 0, 1, 0, 0]
    n_steps = 100

    fiber_profile.builder_profile(dev, sizes, dop_perct, profile_type, materials, alpha, n_steps)

    del fimmap
