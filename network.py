#Esta é a camada de rede
import Packet
from queue import Queue

#função de adiciona os pacotes na queue e faz o random se corrompe o pacote ou não
def udt_send(packet, queue):
    #codigo que corrompe ou não o pacote

    #fim do codigo que corrompe ou não
    queue.put(packet)


def receivd(queue):
    if queue.empty():
        return None
    else:
        return queue.get()