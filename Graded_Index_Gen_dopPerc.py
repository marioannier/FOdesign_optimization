import numpy as np
import matplotlib.pyplot as plt

np.set_printoptions(precision=8)
# set up the fiber values
a1 = 4  # input ("fiber graded index core radius(um)")
alpha = 2.2  # input ("profile power index")
GeO2_SiO2_dop = 0.05  # input ("maximum dopant concentration % (GeSiO2)")
steps = 100 # number of steps in the core area

m = -GeO2_SiO2_dop / (steps ** alpha)  # "pendiente" ecuacion

x = np.arange(0, steps)  # variable x ecuacion parabola
y = np.zeros(steps)  # variable y parabola (porcentajes)

for j in range(steps):
    y[j] = (m * (x[j] ** alpha) + GeO2_SiO2_dop)   # porcentaje j

plt.plot(x, y)
plt.show()
