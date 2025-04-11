import matplotlib.pyplot as plt

x = [0, 1, 2, 3, 4, 5]
y = [0, 1, 4, 9, 16, 25] # = x²
"""
marker='o' -> (circulo)
marker='*' -> (estrela)
marker='x' -> (letra X)
marker='s' -> (quadrado)
marker='d' -> (losango)
"""
plt.plot(x, y, marker='s', linestyle='-', color='r', label='x²')

plt.xlabel('x')
plt.ylabel('y')

plt.title('Gráfico de y = x²')
plt.legend()
plt.grid()

plt.show()