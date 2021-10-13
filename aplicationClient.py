#Esta é a camada de aplicação Sender
import  RDT_2_1
import Packet

def sender_client():
    msg = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    state = '0'
    port = '5002'
    NAK = '0'
    rdt = RDT_2_1.RDT('client', 'localhost', port)
    packet = rdt.rdt_2_1_receive()
    checksum = Packet.calculate_checksum(msg)
    newPackt = Packet.makePacket(0, NAK, checksum)
    while True:
        if state == '0':
            if rdt.send_ready(msg):
                rdt.rdt_2_1_send(newPackt)
                state = '1'
        elif state == '1':
            if rdt.reveid(packet) and (packet.corrupt(packet.msg_S) or packet.isNak()):
                rdt.rdt_2_1_send(newPackt)
            elif rdt.reveid(packet) and not packet.corrupt(packet.msg_S) and packet.isAck():
                state = '2'
        elif state == '2':
            if rdt.send_ready(msg):
                rdt.rdt_2_1_send(newPackt)
                state = '3'
        elif state == '3':
            if rdt.reveid(packet) and (packet.corrupt(packet.msg_S) or packet.isNak()):
                rdt.rdt_2_1_send(newPackt)
            elif rdt.reveid(packet) and not packet.corrupt(packet.msg_S) and packet.isAck():
                state = '1'