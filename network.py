# Esta é a camada de rede
import Packet
from queue import Queue
from time import sleep
import random  # necessário para utilizar o módulo random


# função de adiciona os pacotes na queue e faz o random se corrompe o pacote ou não
def udt_send(packet, queue, range, ini=1):
    # codigo que corrompe ou não o pacote

    r = random.randrange(ini, range)
    if 10 >= r > 5:  # corrompe
        print("Corrompendo pacote")
        msg_corrupt = packet.extract()
        pos = random.randrange(1, 10)
        msg_corrupt[pos] = '$'
        packet.setMsg(msg_corrupt)
    elif 10 < r <= 15:  # perca de pacote
        print("Perca de pacote ")
        packet = None
    elif 15 < r <= 20:  # atraso
        print("Atraso pacote")
        sleep(10)

    # fim do codigo que corrompe ou não
    queue.put(packet)


def receivd(queue):
    if queue.empty():
        return None
    else:
        return queue.get()
