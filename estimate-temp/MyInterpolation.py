import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


# Read data of file
f = open("Commande_Courante.txt", "r")
f.readline()

commande = []
current = []

for line in f:
  data = line.split(", ")
  commande.append(float(data[0]))
  current.append(float(data[1]))


index_to_pop = []
for i in range(len(commande)):
    if commande[i] <= 0:
        index_to_pop.append(i)


commande = [valor for indice, valor in enumerate(commande) if indice not in index_to_pop]
current = [valor for indice, valor in enumerate(current) if indice not in index_to_pop]

# print(commande, current)

# Regression linear by leastsquares
def leastSquares(x, y):
    x = np.array(x)
    y = np.array(y)
    
    # Create the matrix A for the system of equations
    A = x[:, np.newaxis]
    
    # Solve the system of equations using least squares
    m = np.linalg.lstsq(A, y, rcond=None)[0]
    
    return m

#x = np.linspace(0.01, 5, 100)
#y = x**1.5

x = commande
y = current

coefficients = np.polyfit(x, y, 6)
# coefficients = [-6.15824676e+06, 2.50108825e+06, -3.68949792e+05,  2.12011979e+04, -9.01765168e+01,  2.38409422e+01,  7.69204456e-02]

my_curve_fit = np.poly1d(coefficients)

# Gerar pontos para a curva ajustada
x = np.linspace(min(x), max(x), 100)
y = my_curve_fit(x)

plt.plot(commande, current,'b.', x, y,'r')
plt.show()

m1 = leastSquares(x, y)

# plt.plot(x, y, 'r.', x, m1*x)
# plt.show()

def func1(x):
  return m1*x

def find_closest_index(array, value):
  array = np.array(array)
  # Calculate the absolute difference between each element and the given value
  absolute_diff = np.abs(array - value)
  
  # Find the index of the element with the minimum absolute difference
  closest_index = np.argmin(absolute_diff)
  
  return closest_index


def makeGains(x_data, y_data, func):

  y_expected = [float(func(i)) for i in x_data]
  
  

  gains = []
  
  for i in range(len(y_expected)):
    if(x_data[i] != 0):
        new_index = find_closest_index(y_data, y_expected[i])

        g = float(x_data[new_index]) / float(x_data[i])
        # print("gain: ", round(g, 3), "x[index]", round(x[index], 3), "x[i]", round(x[i], 3), "y1", round(y1[index], 3), "y[i]", round(y[i], 3))

        if g < 2 and g > 0.5: 
            gains.append(g) 
        else:
            gains.append(1)
    else:
        gains.append(1)

  return gains


gains = makeGains(x, y, func1)

# print(gains)

xfit = x[6:]
gainsfit = gains[6:]


plt.plot(xfit, gainsfit, 'r.')
plt.show()

popt, pcov = curve_fit(lambda t, a, b: a * np.exp(b * t) + 1, xfit, gainsfit)

a = popt[0]
b = popt[1]
# c = popt[2]

exp_function = lambda x: a * np.exp(b * np.array(x)) + 1

plt.plot(x, gains, 'r.', x, exp_function(x))
plt.show()

print(f"{a} * np.exp({b} * x) + 1")
plt.plot(x/exp_function(x), y, 'b', x, y, "r")
plt.show()

# 0.9069377299857264 * np.exp(-40.850618735955976 * x) + 0.961344151994381

