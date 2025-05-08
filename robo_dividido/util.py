import numpy as np

def definir_estados(front, right, min_dist, parede_dist):
    obstaculo = any(d < min_dist for d in front)
    parede = any(d < parede_dist for d in right)
    livre = all( d > min_dist for d in front )
    media_direita = np.mean(right) if right else float('inf')
    erro = parede_dist - media_direita
    return obstaculo, parede, livre, erro