import numpy as np
import matplotlib.pyplot as plt

np.set_printoptions(precision=8)

# set up the fiber values
a1 = 4  # float(input("fiber graded index core radius(um): "))
a = 1  # float(input("profile power index (1 for triangular): "))
n = 1.45  # float(input("maximum refractive index: "))
n2 = 1.445  # float(input("minimum refractive index (>1.4440236): "))

steps = 100  # number of steps in the core area

x = np.arange(0, a1, a1 / steps)  # variable x ecuacion parabola
y = np.zeros(steps)  # variable y parabola (porcentajes)

A = np.zeros((steps + 3, 4))  # matriz datos
B = A.astype('str')  # cadena

g = a1 / steps  # grosor step
s = '{:.3f}'.format(g)
s1 = " GeO2-SiO2("
s2 = ")"

for j in range(steps):
    y[j] = 6.67677 * n * (1 - 2 * ((n ** 2 - n2 ** 2) / (2 * n ** 2)) * (x[j] / a1) ** a) ** (
            1 / 2) - 9.64142  # porcentaje j
    p = '{:.8f}'.format(y[j])
    B[j, :] = [s, s1 + p + s2, "1", "0"]  # fila j

thickness = ['"a2"', '"a3"', '"SingFibreCladRad"']
ni = ['SiO2("n2")', 'F-SiO2_1(0)', 'SiO2("n2")']

for j in range(3):
    B[j + steps, :] = [thickness[j], ni[j], "0", "0"]
# save in a .txt
np.savetxt('Graded_index.txt', B, delimiter='\t', fmt='%s')
with open('Graded_index.txt') as f:
    print(f.read())

# plot the profile
plt.plot(x, y)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Graded index fiber')
plt.show()
