import numpy as np

def definir_estados(front, right, min_distancia, parede_distancia):
    obstaculo = any(d < min_distancia for d in front)
    parede = any(d < parede_distancia for d in right)
    livre = all(d > min_distancia for d in front)
    
    media_direita = np.mean(right) if right else float('inf')
    erro = parede_distancia - media_direita
    return obstaculo, parede, livre, erro