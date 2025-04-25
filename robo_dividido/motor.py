import sim

# Define a velocidade dos motores
def setar_velocidade(client_ID, left_motor, right_motor, v_esquerda, v_direita):
    sim.simxSetJointTargetVelocity(client_ID, left_motor, v_esquerda, sim.simx_opmode_streaming)
    sim.simxSetJointTargetVelocity(client_ID, right_motor, v_direita, sim.simx_opmode_streaming)

# Para os motores
def parar_motores(client_ID, left_motor, right_motor):
    sim.simxSetJointTargetVelocity(client_ID, left_motor, 0, sim.simx_opmode_streaming)
    sim.simxSetJointTargetVelocity(client_ID, right_motor, 0, sim.simx_opmode_streaming)