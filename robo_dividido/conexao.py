import sim


def conectar_ao_servidor():
    sim.simxFinish(-1)  # Fecha todas as conexões existentes
    client_ID = sim.simxStart('127.0.0.1', 69696, True, True, 5000, 5)
    return client_ID


def obter_handle_motores(client_ID):
    # Obtém o handle dos motores
    _, left_motor = sim.simxGetObjectHandle(
        client_ID, 'Pioneer_p3dx_leftMotor', sim.simx_opmode_blocking)
    _, right_motor = sim.simxGetObjectHandle(
        client_ID, 'Pioneer_p3dx_rightMotor', sim.simx_opmode_blocking)
    return left_motor, right_motor


def desconectar(client_ID):
    sim.simxFinish(client_ID)  # Fecha a conexão com o servidor
