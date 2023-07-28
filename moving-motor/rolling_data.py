import time
import matplotlib.pyplot as plt
import numpy as np

t = np.linspace(1, 10, 400)


w = 4 * np.pi # rad/s
x = np.sin(w*t)


plt.plot(t, x)
plt.show()