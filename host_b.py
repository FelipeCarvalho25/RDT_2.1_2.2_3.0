# Essa é a camada de aplicação Receive
import RDT_2_1
import Packet


def receiver_host_b(queue_a, queue_b):
    # print("HOST B - Instanciando API da camada de transporte para receber dados - RDT 2.1")
    #RDT_2_1.rdt_2_1_receive(queue_a, queue_b )
    #print("HOST B - Instanciando API da camada de transporte para receber dados - RDT 2.2")
    #RDT_2_1.rdt_2_2_receive(queue_a, queue_b)
    print("HOST B - Instanciando API da camada de transporte para receber dados - RDT 3.0")
    RDT_2_1.rdt_3_0_receive(queue_a, queue_b)
    #print(RDT_2_1.rdt_3_0_receive(queue_a, queue_b))

def to_app_layer(msg):
    print("HOST B - Mensagem recebida:" + str(msg))



