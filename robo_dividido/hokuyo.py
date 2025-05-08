import sim
import time

def iniciar_leitura_hokuyo(client_id):
    sim.simxGetStringSignal(client_id, 'Hokuyo', sim.simx_opmode_streaming)
    time.sleep(0.1)

def ler_dados_laser(client_id):
    err, data = sim.simxGetStringSignal(client_id, 'Hokuyo', sim.simx_opmode_buffer)
    if err == sim.simx_return_ok and data:
        return sim.simxUnpackFloats(data)
    return []

def calcular_medidas(laser_data):
    start_angle = -120
    angle_step = 240 / len(laser_data)

    front, right, front_right = [], [], []
    for i, dist in enumerate(laser_data):
        angle = start_angle + i * angle_step

        if -15 <= angle <= 15:
            front.append(dist)
        elif -90 <= angle <= -45:
            right.append(dist)
        elif -30 <= angle <= -15:
            front_right.append(dist)
    return front, right, front_right