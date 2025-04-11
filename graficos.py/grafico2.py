import matplotlib.pyplot as plt
import numpy as np

x = np.random.rand(20) * 10
y = np.random.rand(20) * 10

plt.scatter(x, y, c='red', marker='x', label='Pontos aleatórios')
plt.xlabel('x')
plt.ylabel('y')

plt.title('Gráfico de y = x²')
plt.legend()
plt.grid()

plt.show()