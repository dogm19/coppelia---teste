import time
from estado import Estado
from conexao import conectar_ao_servidor, obter_handle_motores, desconectar
from hokuyo import calcular_medidas, iniciar_leitura_hokuyo, ler_dados_laser
from motor import setar_velocidade, parar_motor
from util import definir_estados

def main():
    min_distance = 0.5
    parede_distancia=0.6
    tempo_giro = 1.5
    tempo_explorar = 60
    tempo_parede_livre = 3

    client_id = conectar_ao_servidor()
    if client_id == -1:
        print("Falha ao conectar ao servidor")
        return
    
    print("Servidor conectado")
    left_motor, right_motor = obter_handle_motores(client_id)
    iniciar_leitura_hokuyo(client_id)

    estado = Estado.EXPLORAR
    tempo_inicio = time.time()
    inicio_giro = None
    parede_livre_inicio = None
    erro_anterior = 0.0

    while time.time() - tempo_inicio < tempo_explorar:
        laser_data = ler_dados_laser(client_id)
        if not laser_data:
            continue

        front, right, front_right = calcular_medidas(laser_data)

        obstaculo, parede_direita, frente_livre, erro_distancia = definir_estados(front, right, min_distance, parede_distancia)

        if estado == Estado.EXPLORAR:
            if obstaculo:
                if parede_direita or erro_distancia > 0.1:
                    estado = Estado.SEGUIR_PAREDE
                    parede_livre_inicio = None
                    print("Mudando estado para: SEGUIR PAREDE")
                else:
                    estado = Estado.GIRAR
                    inicio_giro = time.time()
                    print("Mudando estado para: SEGUIR GIRAR")
            elif parede_direita and abs(erro_distancia) > 0.3:
                    estado = Estado.SEGUIR_PAREDE
                    parede_livre_inicio = None
                    print("Mudando estado para: SEGUIR PAREDE")
            else:
                setar_velocidade(client_id, left_motor, right_motor, 2.0, 2.0)
        elif estado == Estado.GIRAR:
            setar_velocidade(client_id, left_motor, right_motor, -1.5, 1.5)
            if time.time() - inicio_giro >= tempo_giro:
                estado = Estado.SEGUIR_PAREDE
                print("Giro completo. estado para: SEGUIR PAREDE")
        elif estado == Estado.SEGUIR_PAREDE:
            if obstaculo:
                setar_velocidade(client_id, left_motor, right_motor, -1.5, 1.5)
                print("Obstáculo a frente. Girando à esquerda")
            else:
                if not parede_direita and frente_livre:
                    setar_velocidade(client_id, left_motor, right_motor, 1.2, 1.8)
                    print("Parede sumiu à direita, Curva suave a esquerda")
                else:
                    Kp = 2.5
                    Kd = 1.0
                    derivada = erro_distancia - erro_anterior
                    ajuste = Kp * erro_distancia + Kd * derivada
                    erro_anterior = erro_distancia

                    vel_base=2.0
                    if abs(erro_distancia) > 0.2:
                        vel_base=1.6

                    vel_left = max(min(vel_base - ajuste, 2.5), -2.5)
                    vel_right = max(min(vel_base + ajuste, 2.5), -2.5)

                    setar_velocidade(client_id, left_motor, right_motor, vel_left, vel_right)
            if frente_livre:
                if parede_livre_inicio is None:
                    parede_livre_inicio = time.time()
                elif time.time() - parede_livre_inicio > tempo_parede_livre:
                    estado = Estado.EXPLORAR
                    print("Frente livre, Voltando para EXPLORAR")
            else:
                parede_livre_inicio = None
        time.sleep(0.1)
    
    print("tempo esgotado Mudado para PARE")
    parar_motor(client_id, left_motor, right_motor)
    desconectar(client_id)
    print("Programa finalizado")

if __name__ == '__main__':
    main()