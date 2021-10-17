# Essa é a camada de aplicação Receive
import RDT_2_1
import Packet


def receiver_host_b(queue, event):
    print("HOST B - Instanciando API da camada de transporte para receber dados")
    print(RDT_2_1.rdt_2_1_receive(queue, event))

def to_app_layer(msg):
    print("HOST B - Mensagem recebida:" + str(msg))



