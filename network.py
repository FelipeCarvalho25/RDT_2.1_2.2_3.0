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
        print("NETWORK - Corrompendo pacote")
        msg_S = packet.extract()
        msg_corrupt = msg_S[0:len(msg_S)]
        pos = random.randrange(1, 10)
        msg_corrupt[pos] = '$'
        pckt_snd = packet
        pckt_snd.setMsg(msg_corrupt)
    elif 10 < r <= 15:  # perca de pacote
        print("NETWORK - Perca de pacote ")
        pckt_snd = None
    elif 15 < r <= 20:  # atraso
        print("NETWORK - Atraso pacote")
        pos = random.randrange(5, 15)
        sleep(pos)
        pckt_snd = packet
    else:
        print("NETWORK - Pacote normal")
        pckt_snd = packet

    # fim do codigo que corrompe ou não
    queue.put(pckt_snd)

    sleep(5)


def udt_receivd(queue):
    sleep(2)
    if queue.empty():
        return None
    else:
        return queue.get()
