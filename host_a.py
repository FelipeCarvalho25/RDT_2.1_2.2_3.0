# Esta é a camada de aplicação Sender
import RDT_2_1
import Packet


def host_a_sender(queue_a, queue_b):
    msg = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    print("HOST A - Instanciando camada de transporte para enviar dados... RDT 2.1")
    RDT_2_1.rdt_2_1_send(msg,queue_a, queue_b)
    #print("HOST A - Instanciando camada de transporte para enviar dados... RDT 2.2")
    #print("HOST A - Enviando Mensagem")
    #RDT_2_1.rdt_2_2_send(msg, queue, event)
    #print("HOST A - Instanciando camada de transporte para enviar dados... RDT 3.0")
    #print("HOST A - Enviando Mensagem")
    #RDT_2_1.rdt_3_0_send(msg, queue, event)
    #RDT_2_1.rdt_3_0_send(msg,queue, event)







