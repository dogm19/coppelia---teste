import sim


def conectar_ao_servidor():
    sim.simxFinish(-1)
    client_id = sim.simxStart('127.0.0.1', 69696, True, True, 5000, 5)
    return client_id


def obter_handle_motores(client_id):
    _, left_motor = sim.simxGetObjectHandle(
        client_id, 'Pioneer_p3dx_leftMotor', sim.simx_opmode_blocking)
    _, right_motor = sim.simxGetObjectHandle(
        client_id, 'Pioneer_p3dx_rightMotor', sim.simx_opmode_blocking)
    return left_motor, right_motor


def desconectar(client_id):
    sim.simxFinish(client_id)
