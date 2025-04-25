import sim
import time

# Inicia a leitura do Hokuyo


def iniciar_leitura_hokuyo(client_ID):
    sim.simxGetIntegerSignal(client_ID, 'Hokuyo', sim.simx_opmode_streaming)
    time.sleep(0.1)  # Aguarda um pouco para garantir que a leitura comece


def ler_dados_laser(client_ID):
    err, data = sim.simxGetIntegerSignal(
        client_ID, 'Hokuyo', 1, sim.simx_opmode_buffer)
    if err == sim.simx_return_ok and data:
        return sim.simxUnpackFloats(data)
    return []


def calcular_medidas(laser_data):
    start_angle = -120
    angle_step = 240 / len(laser_data)

    front, right, front_right = [], [], []
    for i, distance in enumerate(laser_data):
      #         -120 + 0 * 240
        angle = start_angle + i * angle_step

        if -15 <= angle <= 15:
            front.append(distance)
        elif 90 < angle <= -45:
            right.append(distance)
        elif -30 <= angle < -15:
            front_right.append(distance)
    return front, right, front_right
