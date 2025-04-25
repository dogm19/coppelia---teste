try:
    import sim
except:
    print("Erro ao importar a biblioteca")

import time
import numpy as np
from enum import Enum


class Estado(Enum):
    MOVIMENTO = 1
    VIRAR_ESQUERDA = 2
    VIRAR_DIREITA = 3


sim.simxFinish(-1)  # fecha as conexões anteriores
clientID = sim.simxStart('127.0.0.1', 69696, True, True, 5000, 5)

if clientID != -1:
    print("Conexão estabelecida com o simulador")
    # sim.simx_opmode_blocking fica travado até conectar
    _, left_motor = sim.simxGetObjectHandle(
        clientID, 'Pioneer_p3dx_leftMotor', sim.simx_opmode_blocking)
    _, right_motor = sim.simxGetObjectHandle(
        clientID, 'Pioneer_p3dx_rightMotor', sim.simx_opmode_blocking)
    _, _ = sim.simxGetStringSignal(
        clientID, 'Hokuyo', sim.simx_opmode_streaming)
    time.sleep(0.1)

    estado = Estado.MOVIMENTO  # Estado inicial
    DURATION = 60  # duração do movimento em segundos
    DESVIO_DURACAO = 1  # tempo de desvio em segundos
    desvio_inicio = 0  # tempo de início do desvio

    start_time = time.time()

    # sensores simx_opmode_streaming troca de informação do sensor com python
    while time.time() - start_time < DURATION:

        # Lê os dados do sensor
        err, data = sim.simxGetStringSignal(
            clientID, 'Hokuyo', sim.simx_opmode_buffer)

        if err == sim.simx_return_ok and data:
            laser_data = sim.simxUnpackFloats(data)
            # Converte os dados do laser para um array numpy
            num_readings = len(laser_data)

            if num_readings == 0:
                continue

            start_angle = -120
            angle_step = 240 / num_readings

            front_dist = []
            left_dist = []
            right_dist = []

            for i, distance in enumerate(laser_data):
                angle = start_angle + i * angle_step

                if -20 <= angle <= 20:
                    front_dist.append(distance)

                elif 45 < angle <= 90:
                    left_dist.append(distance)

                elif -90 <= angle < -45:
                    right_dist.append(distance)

            MIN_DISTANCE = 0.5  # distância mínima para considerar um obstáculo

            obstacle_ahead = any(d < MIN_DISTANCE for d in front_dist)

            if estado == Estado.MOVIMENTO:

                if obstacle_ahead:
                    avg_left = np.mean(left_dist) if left_dist else 0
                    avg_right = np.mean(right_dist) if right_dist else 0

                    if avg_left > avg_right:
                        estado = Estado.VIRAR_ESQUERDA
                        print("Vira para a esquerda")

                    else:
                        estado = Estado.VIRAR_DIREITA
                        print("Vira para a direita")

                    desvio_inicio = time.time()  # Inicia o tempo de desvio

                else:
                    # Move para frente
                    sim.simxSetJointTargetVelocity(
                        clientID, left_motor, 2.0, sim.simx_opmode_streaming)  # motor esquerdo
                    sim.simxSetJointTargetVelocity(
                        clientID, right_motor, 2.0, sim.simx_opmode_streaming)  # motor direito
            elif estado == Estado.VIRAR_ESQUERDA:
                sim.simxSetJointTargetVelocity(
                    clientID, left_motor, -1.5, sim.simx_opmode_streaming)
                sim.simxSetJointTargetVelocity(
                    clientID, right_motor, 1.5, sim.simx_opmode_streaming)

                if time.time() - desvio_inicio >= DESVIO_DURACAO:
                    estado = Estado.MOVIMENTO
                    print("Retorna ao movimento")

            elif estado == Estado.VIRAR_DIREITA:
                sim.simxSetJointTargetVelocity(
                    clientID, left_motor, 1.5, sim.simx_opmode_streaming)
                sim.simxSetJointTargetVelocity(
                    clientID, right_motor, -1.5, sim.simx_opmode_streaming)

                if time.time() - desvio_inicio >= DESVIO_DURACAO:
                    estado = Estado.MOVIMENTO
                    print("Retorna ao movimento")

        time.sleep(0.1)

    sim.simxSetJointTargetVelocity(
        clientID, left_motor, 0, sim.simx_opmode_blocking)  # motor esquerdo
    sim.simxSetJointTargetVelocity(
        clientID, right_motor, 0, sim.simx_opmode_blocking)  # motor direito
    sim.simxFinish(clientID)  # fecha a conexão com o simulador

else:
    print("Falha na Conexao com o simulador")

print("programa finalizado")
