#Esta é a camada de transporte
import network
import Packet
import time

class RDT_2_1:

    def __init__(self, role_S, server_S, port):
        self.network = network.NetworkLayer(role_S, server_S, port)

    def disconnect(self):
        self.network.disconnect()

    def rdt_2_1_send(self, msg_S):
        pass

    def rdt_2_1_receive(self):
        pass

    def rdt_3_0_send(self, msg_S):
        pass

    def rdt_3_0_receive(self):
        pass