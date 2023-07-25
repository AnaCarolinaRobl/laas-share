import math
import matplotlib.pyplot as plt
import numpy as np
import time 

W = 2

senos = []
t = 0
ts = []

while True:
    t += 1
    senos.append(math.sin(t * W)*2 + 5)
    ts.append(t)
    print(ts, senos)

    plt.plot(ts, senos)
    plt.show()