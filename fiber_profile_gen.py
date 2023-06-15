import numpy as np
import matplotlib.pyplot as plt


class fiber_profile_gen:

    def __init__(self, profile_name):
        self.profile_name = profile_name

    def rc_refindex(self, a1, n1, n2, alpha, steps):
        # based on : https://doi.org/10.1016/j.yofte.2021.102777
        # Multicore raised cosine fibers for next generation space division multiplexing systems
        # refractive index relation with GiO2-SiO2 percentage Percentage = -6.67677 * refractive_index + 9.64142
        self.a1 = a1
        self.n1 = n1
        self.n2 = n2
        self.alpha = alpha  # should be btw 0 and <1
        self.steps = steps

        x = np.arange(0, self.a1, self.a1 / self.steps)
        y = np.zeros(self.steps)
        perc = np.zeros(self.steps)

        for j, r in zip(range(self.steps), x):
            if r <= ((1 - self.alpha) * (self.a1 / 2)):
                y[j] = self.n1
            elif ((1 - self.alpha) * (self.a1 / 2)) < r <= ((1 + self.alpha) * (self.a1 / 2)):
                # y[j] = 1 / (2 * (self.n1 - self.n2)) * (
                #         1 + np.cos((r / (self.a1 * self.alpha)) * (np.pi - ((self.a1 * (1 - self.alpha)) / 2))))
                y[j] = self.n2 + 0.5 * (self.n1 - self.n2) * (
                        1 + np.cos(np.pi / (self.a1 * self.alpha) * (r - self.a1 * 0.5 * (1 - self.alpha))))
            else:
                y[j] = self.n2

            perc[j] = -6.68002672 * y[j] + 9.7460532

        plt.plot(x,perc)
        plt.xlabel('radius')
        plt.ylabel('dop_perc_GeO2-SiO2')
        plt.title('Graded index fiber')
        plt.show()

        return perc

    def graded_refindex(self, a1, n1, n2, alpha, steps):
        # refractive index relation with GiO2-SiO2 percentage Percentage = -6.67677 * refractive_index +9.64142
        self.a1 = a1
        self.n1 = n1
        self.n2 = n2
        self.alpha = alpha
        self.steps = steps
        x = np.arange(0, self.a1, self.a1 / self.steps)
        y = np.zeros(self.steps)
        perc = np.zeros(self.steps)
        delta = (self.n1**2-self.n2**2)/(2*self.n1**2)

        for j, r in zip(range(self.steps), x):
            y[j] = (self.n1 * np.sqrt(1-2*delta*(r/self.a1)**self.alpha))
            perc[j] = -6.68002672*y[j] + 9.7460532

        plt.plot(x, perc)
        plt.xlabel('radius')
        plt.ylabel('dop_perc_GeO2-SiO2')
        plt.title('Graded index fiber')
        plt.show()


        return perc
