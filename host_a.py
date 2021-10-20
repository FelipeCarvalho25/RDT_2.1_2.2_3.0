# Esta é a camada de aplicação Sender
import RDT_2_1



def host_a_sender(queue_a, queue_b):
    msg = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j','k','l','m','n','o', 'p','q', 'r', 's','t']
    print("HOST A - Instanciando camada de transporte para enviar dados... RDT 2.1")
    RDT_2_1.rdt_2_1_send(msg,queue_a, queue_b)
    #print("HOST A - Instanciando camada de transporte para enviar dados... RDT 2.2")
    #RDT_2_1.rdt_2_2_send(msg, queue_a, queue_b)
    #print("HOST A - Instanciando camada de transporte para enviar dados... RDT 3.0")
    #RDT_2_1.rdt_3_0_send(msg, queue_a, queue_b)
    #RDT_2_1.rdt_3_0_send(msg,queue, event)







