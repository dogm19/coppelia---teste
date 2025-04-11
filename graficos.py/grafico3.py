import matplotlib.pyplot as plt

categorias = ['A', 'B', 'C', 'D']
valores = [10, 25, 7, 15]

plt.bar(categorias, valores, color=['red', 'blue', 'green', 'yellow'])
for i, valor in enumerate(valores):
  plt.text(i, valor + 0.5, str(valor), ha='center', fontsize=10, fontweight='bold')
  
plt.xlabel('x')
plt.ylabel('y')

plt.title('grafico de barras')
plt.legend()
#plt.grid()

plt.show()