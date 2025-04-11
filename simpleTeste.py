try:
    import sim
except:
    print("Erro ao importar a biblioteca")

import time

sim.simxFinish(-1)  # fecha as conexões anteriores

clientID = sim.simxStart('127.0.0.1', 69696, True, True, 5000, 5)

# Aguarda até que o simulador seja inicializado
if clientID != -1:
    print("Conexão estabelecida com o simulador")

    # sim.simx_opmode_blocking fica travado até conectar
    _, left_motor = sim.simxGetObjectHandle(
        clientID, 'Pioneer_p3dx_leftMotor', sim.simx_opmode_blocking)
    _, right_motor = sim.simxGetObjectHandle(
        clientID, 'Pioneer_p3dx_rightMotor', sim.simx_opmode_blocking)

    # sensores simx_opmode_streaming troca de informação do sensor com python
    _, sensor_quatro = sim.simxGetObjectHandle(
        clientID, 'Pioneer_p3dx_ultrasonicSensor4', sim.simx_opmode_blocking)
    sim.simxReadProximitySensor(
        clientID, sensor_quatro, sim.simx_opmode_streaming)
    _, sensor_cinco = sim.simxGetObjectHandle(
        clientID, 'Pioneer_p3dx_ultrasonicSensor5', sim.simx_opmode_blocking)
    sim.simxReadProximitySensor(
        clientID, sensor_cinco, sim.simx_opmode_streaming)
    _, sensor_seis = sim.simxGetObjectHandle(
        clientID, 'Pioneer_p3dx_ultrasonicSensor6', sim.simx_opmode_blocking)
    sim.simxReadProximitySensor(
        clientID, sensor_seis, sim.simx_opmode_streaming)
    _, sensor_sete = sim.simxGetObjectHandle(
        clientID, 'Pioneer_p3dx_ultrasonicSensor7', sim.simx_opmode_blocking)
    sim.simxReadProximitySensor(
        clientID, sensor_sete, sim.simx_opmode_streaming)

    # Definindo funções para os motores das rodas se moverem para frente

    def motorFrente(speed=2.0, duration=0.5):
        sim.simxSetJointTargetVelocity(
            clientID, left_motor, speed, sim.simx_opmode_streaming)  # motor esquerdo
        sim.simxSetJointTargetVelocity(
            clientID, right_motor, speed, sim.simx_opmode_streaming)  # motor direito
        time.sleep(duration)  # duração da pausa do movimento

    def moverEsquerda(speed=0.5, duration=1.0):
        sim.simxSetJointTargetVelocity(
            clientID, left_motor, -speed, sim.simx_opmode_streaming)  # motor esquerdo
        sim.simxSetJointTargetVelocity(
            clientID, right_motor, speed, sim.simx_opmode_streaming)  # motor direito
        time.sleep(duration)  # duração da pausa do movimento

    def moverDireita(speed=2.0, duration=2.0):
        sim.simxSetJointTargetVelocity(
            clientID, left_motor, speed, sim.simx_opmode_streaming)  # motor esquerdo
        sim.simxSetJointTargetVelocity(
            clientID, right_motor, -speed, sim.simx_opmode_streaming)  # motor direito
        time.sleep(duration)  # duração da pausa do movimento

    def stop():
        sim.simxSetJointTargetVelocity(
            clientID, left_motor, 0, sim.simx_opmode_blocking)
        sim.simxSetJointTargetVelocity(
            clientID, right_motor, 0, sim.simx_opmode_blocking)

    start_time = time.time()
    while time.time() - start_time < 60:
        motorFrente()
        _, detectionState1, detectionPoint1, _, _ = sim.simxReadProximitySensor(
        clientID, sensor_quatro, sim.simx_opmode_streaming)
        _, detectionState2, detectionPoint2, _, _ = sim.simxReadProximitySensor(
        clientID, sensor_cinco, sim.simx_opmode_streaming)
        _, detectionState3, detectionPoint3, _, _ = sim.simxReadProximitySensor(
        clientID, sensor_seis, sim.simx_opmode_streaming)
        _, detectionState4, detectionPoint4, _, _ = sim.simxReadProximitySensor(
        clientID, sensor_sete, sim.simx_opmode_streaming)

        if detectionState1:
            x, y, z = detectionPoint1
            if z < 0.9:
                moverEsquerda()
        if detectionState2:
            x, y, z = detectionPoint2
            if z < 0.9:
                moverEsquerda()
        if detectionState3:
            x, y, z = detectionPoint3
            if z < 0.9:
                moverEsquerda()
        if detectionState4:
            x, y, z = detectionPoint4
            if z < 0.9:
                moverEsquerda()
        motorFrente()
        time.sleep(0.5)

    # for _ in range(3):
    #   motorFrente()
    #   moverDireita()
    #   moverEsquerda()
    stop()
else:
    print("Erro ao conectar com o simulador")

print("Programa finalizado")
