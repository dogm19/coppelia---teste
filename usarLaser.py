try:
    import sim
except:
    print("Erro ao importar a biblioteca")

import time
import math
import matplotlib.pyplot as plt

sim.simxFinish(-1)  # fecha as conexões anteriores

clientID = sim.simxStart('127.0.0.1', 69696, True, True, 5000, 5)

# Aguarda até que o simulador seja inicializado
if clientID != -1:
    print("Conexão estabelecida com o simulador")

    status, data = sim.simxGetStringSignal(
        clientID, 'Hokuyo', sim.simx_opmode_blocking)

    if status == sim.simx_return_ok and data:
        # retorna uma lista de valores float
        laser_data = sim.simxUnpackFloats(data)

        num_reading = len(laser_data)
        if num_reading == 0:
            print("Nenhum dado do laser")
            sim.simxFinish(-1)
            exit()

        # por padrão o fasthokuyo cobre 240º
        # de -120º a 120º
        start_angle = -120
        end_angle = 120
        angle_step = 240/num_reading

        x_coords = []
        y_coords = []

        for i, distance in enumerate(laser_data):
            # primeiro converter o ângulo para radianos
            angle = math.radians(start_angle + i*angle_step)
            # calcular as coordenadas x e y do ponto no plano cartesiano sen e cos
            x = distance * math.cos(angle)
            y = distance * math.sin(angle)
            x_coords.append(x)
            y_coords.append(y)

        # plotar os dados do laser
        plt.figure(figsize=(6, 6), dpi=100)
        plt.scatter(x_coords, y_coords, marker='o',
                    color='b', label='Laser lido')
        plt.plot(0, 0, 'k>', markersize=10, label='Robô')

        plt.xlabel([-5.5, 5.5])
        plt.ylabel([-5.5, 5.5])
        plt.grid()
        plt.xlabel('x -> (m)')
        plt.ylabel('y -> (m)')
        plt.title('Mapa do ambiente')
        plt.legend()
        plt.show()
    else:
        print("Erro ao ler dados do laser")

    sim.simxFinish(clientID)

print("Conexão encerrada")
