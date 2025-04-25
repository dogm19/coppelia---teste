import time
from estado import Estado
from conexao import conectar_ao_servidor, obter_handle_motores, desconectar
from hokuyo import iniciar_leitura_hokuyo, ler_dados_laser, calcular_medidas
from motor import setar_velocidade, parar_motores
from util import definir_estados


def main():
    min_distancia = 0.5  # Distância mínima em metros
    parede_distancia = 0.6  # Distância da parede em metros
    tempo_giro = 1.5  # Tempo de giro em segundos
    tempo_explorar = 60  # Tempo de exploração em segundos
    tempo_parede_livre = 3  # Tempo de seguir a parede livre em segundos

    client_ID = conectar_ao_servidor()
    if client_ID == -1:
        print("Erro ao conectar ao servidor.")
        return
    print("Conectado ao servidor.")
    left_motor, right_motor = obter_handle_motores(client_ID)
    iniciar_leitura_hokuyo(client_ID)

    estado = Estado.EXPLORAR
    tempo_inicial = time.time()
    inicio_giro = None
    parede_livre_inicio = None
    erro_anterior = 0.0

    while time.time() - tempo_inicial < tempo_explorar:
        laser_data = ler_dados_laser(client_ID)
        if not laser_data:
            continue
        front, right, front_right = calcular_medidas(laser_data)

        obstaculo, parede_direita, frente_livre, erro_distancia = definir_estados(
            front, right, min_distancia, parede_distancia)

        if estado == Estado.EXPLORAR:
            if obstaculo:
                if parede_direita or erro_distancia > 0.1:
                    estado = Estado.SEGUIR_PAREDE
                    parede_livre_inicio = None
                    print("Mudando para o estado SEGUIR_PAREDE")
                else:
                    estado = Estado.GIRO
                    inicio_giro = time.time()
                    print("Mudando para o estado GIRO")
            elif parede_direita and abs(erro_distancia) > 0.3:
                estado = Estado.SEGUIR_PAREDE
                parede_livre_inicio = None
                print("Mudando para o estado SEGUIR_PAREDE")
            else:
                setar_velocidade(client_ID, left_motor, right_motor, 2.0, 2.0)
        elif estado == Estado.GIRAR:
            setar_velocidade(client_ID, left_motor, right_motor, -1.5, 1.5)
            if time.time() - inicio_giro >= tempo_giro:
                estado = Estado.SEGUIR_PAREDE
                print("Giro completo, mudando para SEGUIR_PAREDE")
        elif estado == Estado.SEGUIR_PAREDE:
            if obstaculo:
                setar_velocidade(client_ID, left_motor, right_motor, -1.5, 1.5)
                print("obstaculo a frente. girando a esquerda")
            else:
                if not parede_direita and frente_livre:
                    setar_velocidade(client_ID, left_motor, right_motor, 1.2, 1.8)
                    print("Seguindo a parede livre a direita, curva a esquerda")
                else:
                    Kp = 2.5
                    Kd = 1.0
                    derivada = erro_distancia - erro_anterior
                    ajuste = Kp * erro_distancia + Kd * derivada
                    erro_anterior = erro_distancia

                    vel_base = 2.0
                    if abs(erro_distancia) > 0.2:
                        vel_base = 1.6
                    vel_left = max(min(vel_base - ajuste, 2.5), -2.5)
                    vel_right = max(min(vel_base + ajuste, 2.5), -2.5)
                    
                    setar_velocidade(client_ID, left_motor, right_motor, vel_left, vel_right)
                    print(f"Seguindo a parede, ajustando velocidades: Esquerda: {vel_left}, Direita: {vel_right}")
            if frente_livre:
                if parede_livre_inicio is None:
                    parede_livre_inicio = time.time()
                elif time.time() - parede_livre_inicio > tempo_parede_livre:
                    estado = Estado.EXPLORAR
                    print("Mudando para o estado EXPLORAR")
            else:
                parede_livre_inicio = None
                print("Parede livre, aguardando")
        time.sleep(0.1)
        
    parar_motores(client_ID, left_motor, right_motor)
    desconectar()
    print("Desconectado do servidor.")

if __name__ == "__main__":
    main()
