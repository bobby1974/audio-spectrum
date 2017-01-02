import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0.1, 2*np.pi, 10)

baseline = plt.stem(x, np.cos(x), '-.')

#plt.setp(markerline, 'markerfacecolor', 'b')

plt.show()