import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-10, 10, 100)
y = x**2

plt.figure(figsize=(8, 6))
plt.plot(x, y, label='y = x^2', color='red', linestyle='-', linewidth=2)
plt.title('grafico de linha')

plt.xlabel('x')
plt.ylabel('y')

plt.legend()
plt.grid()
plt.show()