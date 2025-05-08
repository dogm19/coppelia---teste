import sim

def setar_velocidade(client_id, left_motor, right_motor, v_left, v_right):
    sim.simxSetJointTargetVelocity(client_id, left_motor, v_left, sim.simx_opmode_streaming)
    sim.simxSetJointTargetVelocity(client_id, right_motor, v_right, sim.simx_opmode_streaming)

def parar_motor(client_id, left_motor, right_motor):
    setar_velocidade(client_id, left_motor, right_motor, 0, 0)