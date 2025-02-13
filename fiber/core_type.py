
class FiberParameters:
    def __init__(self, sizes=[4, 5, 5, 30], dop_perct=[0.1, 0, 0, 0],
                 profile_type=['Constant', 'Constant', 'Constant', 'Constant'],
                 materials=['GeO2-SiO2', 'SiO2', 'SiO2', 'SiO2'], alphas=[0, 0, 0, 0], n_steps=2,
                 dev="app.subnodes[1].subnodes[1]"):
        self.sizes = sizes
        self.dop_perct = dop_perct
        self.profile_type = profile_type
        self.materials = materials
        self.alphas = alphas
        self.n_steps = n_steps
        self.dev = dev

    def core_type_meth(self, core_type):
        # Define parameters for different core types
        dev = "app.subnodes[1].subnodes[1]"
        match core_type:
            case "step index":
                sizes = [4, 5, 5, 30]
                dop_perct = [0.1, 0, 0, 0]
                profile_type = ['Constant', 'Constant', 'Constant', 'Constant']
                materials = ['GeO2-SiO2', 'SiO2', 'SiO2', 'SiO2']
                alphas = [0, 0, 0, 0]
                n_steps = 2

            case "step index with trench F-SiO2_1":
                sizes = [4, 3, 3, 30]
                dop_perct = [0.1, 0, 0, 0]
                profile_type = ['Constant', 'Constant', 'Constant', 'Constant']
                materials = ['GeO2-SiO2', 'SiO2', 'F-SiO2_1', 'SiO2']
                alphas = [0, 0, 0, 0]
                n_steps = 2

            case "step index with trench F-SiO2_2":
                sizes = [4, 3, 3, 30]
                dop_perct = [0.1, 0, 0, 0]
                profile_type = ['Constant', 'Constant', 'Constant', 'Constant']
                materials = ['GeO2-SiO2', 'SiO2', 'F-SiO2_2', 'SiO2']
                alphas = [0, 0, 0, 0]
                n_steps = 2

            case "W shape F-SiO2_1":
                sizes = [4, 3, 5, 30]
                dop_perct = [0.1, 0, 0, 0]
                profile_type = ['Constant', 'Constant', 'Constant', 'Constant']
                materials = ['GeO2-SiO2', 'F-SiO2_1', 'SiO2', 'SiO2']
                alphas = [0, 0, 0, 0]
                n_steps = 2

            case "W shape F-SiO2_2":
                sizes = [4, 3, 5, 30]
                dop_perct = [0.1, 0, 0, 0]
                profile_type = ['Constant', 'Constant', 'Constant', 'Constant']
                materials = ['GeO2-SiO2', 'F-SiO2_2', 'SiO2', 'SiO2']
                alphas = [0, 0, 0, 0]
                n_steps = 2

            case "three layers all GeO2 dp":
                sizes = [4, 3, 5, 30]
                dop_perct = [0.1, 0.04, 0.02, 0]
                profile_type = ['Constant', 'Constant', 'Constant', 'Constant']
                materials = ['GeO2-SiO2', 'GeO2-SiO2', 'GeO2-SiO2', 'SiO2']
                alphas = [0, 0, 0, 0]
                n_steps = 2

            case _:
                raise ValueError(f"Unsupported core type: {core_type}")

        return FiberParameters(sizes, dop_perct, profile_type, materials, alphas, n_steps, dev)
