# Esta é a camada de aplicação Sender
import RDT_2_1
import Packet


def host_a_sender(queue, event):
    msg = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    print("HOST A - Instanciando camada de transporte para enviar dados...")
    print("HOST A - Enviando Mensagem")
    RDT_2_1.rdt_2_1_send(msg,queue, event)
    #RDT_2_1.rdt_3_0_send(msg,queue, event)







