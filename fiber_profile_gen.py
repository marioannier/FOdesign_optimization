import numpy as np
import matplotlib.pyplot as plt


class FiberProfileGen:
    def __init__(self):
        # write initial values
        pass

    def rc_refindex(self, alpha, dopa_max, steps):
        # based on : https://doi.org/10.1016/j.yofte.2021.102777
        # Multicore raised cosine fibers for next generation space division multiplexing systems
        # refractive index relation with GiO2-SiO2 percentage Percentage = -6.67677 * refractive_index + 9.64142
        self.n1 = (dopa_max + 9.6495) / 6.6823
        self.n2 = 9.6495 / 6.6823  # zero dopant n2 = 1.4440236217
        self.alpha = alpha  # should be btw 0 and <1
        self.steps = steps

        x = np.arange(0, self.steps, 1)
        y = np.zeros(self.steps)
        perc = np.zeros(self.steps)

        for j in range(self.steps):
            if j <= ((1 - self.alpha) * (self.steps / 2)):
                y[j] = self.n1
            elif ((1 - self.alpha) * (self.steps / 2)) < j <= ((1 + self.alpha) * (self.steps / 2)):
                y[j] = self.n2 + 0.5 * (self.n1 - self.n2) * (
                        1 + np.cos(np.pi / (self.steps * self.alpha) * (j - self.steps * 0.5 * (1 - self.alpha))))
            else:
                y[j] = self.n2

            perc[j] = 6.6823 * y[j] - 9.6495
        return perc.round(4)

    def graded_refindex(self, alpha, dopa_max, steps):
        # refractive index relation with GiO2-SiO2 percentage Percentage = -6.67677 * refractive_index + 9.64142
        self.n1 = (dopa_max + 9.6495) / 6.6823
        self.n2 = 9.6495 / 6.6823  # zero dopant n2 = 1.4440236217
        self.alpha = alpha  # should be btw 0 and <1
        self.steps = steps

        x = np.arange(0, self.steps, 1)
        y = np.zeros(self.steps)
        perc = np.zeros(self.steps)

        delta = (self.n1 ** 2 - self.n2 ** 2) / (2 * self.n1 ** 2)

        for j in range(self.steps):
            y[j] = (self.n1 * np.sqrt(1 - 2 * delta * (j / self.steps) ** self.alpha))
            perc[j] = 6.6823 * y[j] - 9.6495

        return perc.round(4)
