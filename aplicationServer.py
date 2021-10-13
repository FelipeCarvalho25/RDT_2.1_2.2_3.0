#Essa é a camada de aplicação Receive
import  RDT_2_1
import Packet

def receiver_server(packet):
    state = '0'
    port = '5002'
    NAK = '0'
    rdt = RDT_2_1.RDT('server', None, port)
    while True:
        if state == '0':
            if rdt.reveid(packet) and packet.corrupt(packet.msg_S):
                checksum = Packet.calculate_checksum(packet.msg_S)
                newPackt = Packet.makePacket(NAK, checksum)
                rdt.rdt_2_1_send(newPackt)
            elif rdt.reveid(packet) and not packet.corrupt(packet.msg_S) and packet.has_seq() == '1':
                checksum = Packet.calculate_checksum(packet.msg_S)
                newPackt = Packet.makePacket(NAK, checksum)
                rdt.rdt_2_1_send(newPackt)
            elif rdt.reveid(packet) and not packet.corrupt(packet.msg_S) and packet.has_seq() == '0':
                data = packet.extract()
                deliver_data(data)
                checksum = Packet.calculate_checksum(packet.msg_S)
                newPackt = Packet.makePacket(NAK, checksum)
                rdt.rdt_2_1_send(newPackt)
                state = '1'
        elif state == '1':
            if rdt.reveid(packet) and packet.corrupt(packet.msg_S):
                checksum = Packet.calculate_checksum(packet.msg_S)
                newPackt = Packet.makePacket(NAK, checksum)
                rdt.rdt_2_1_send(newPackt)
            elif rdt.reveid(packet) and not packet.corrupt(packet.msg_S) and packet.has_seq() == '0':
                checksum = Packet.calculate_checksum(packet.msg_S)
                newPackt = Packet.makePacket(NAK, checksum)
                rdt.rdt_2_1_send(newPackt)
            elif rdt.reveid(packet) and not packet.corrupt(packet.msg_S) and packet.has_seq() == '1':
                data = packet.extract()
                deliver_data(data)
                checksum = Packet.calculate_checksum(packet.msg_S)
                newPackt = Packet.makePacket(NAK, checksum)
                rdt.rdt_2_1_send(newPackt)
                state = '1'

def deliver_data(data):
    print("Receive msg" + data)
