# Esta é a camada de transporte
import network
import Packet
import time
from queue import Queue


def reveid():
    return 'msg'


def deliver_data(msg, data):
    return data + msg


def rdt_2_1_send(msg_S):
    state = '0'
    rcv_packt = None
    while True:
        if state == '0':
            snd_packt = Packet.Packet(0, msg_S, '0')
            # if RDT_2_1.send_ready(msg_S):
            network.udt_send(snd_packt)
            state = '1'
        elif state == '1':
            snd_packt = Packet.Packet(0, msg_S, '0')
            rcv_packt = reveid(rcv_packt)
            if not (rcv_packt is None) and (
                    rcv_packt.corrupt(rcv_packt.msg_S, rcv_packt.check_sum) or rcv_packt.isNak()):
                network.udt_send(snd_packt)
            elif not (rcv_packt is None) and not rcv_packt.corrupt(rcv_packt.msg_S) and rcv_packt.isAck():
                state = '2'
        elif state == '2':
            snd_packt = Packet.Packet(1, msg_S, '1')
            network.udt_send(snd_packt)
            state = '3'
        elif state == '3':
            snd_packt = Packet.Packet(1, msg_S, '1')
            rcv_packt = reveid(rcv_packt)
            if not (rcv_packt is None) and (rcv_packt.corrupt(rcv_packt.msg_S) or rcv_packt.isNak()):
                network.udt_send(snd_packt)
            elif not (rcv_packt is None) and not rcv_packt.corrupt(rcv_packt.msg_S) and rcv_packt.isAck():
                state = '1'


def rdt_2_1_receive():
    state = '0'
    NAK = 'NAK'
    ACK = 'ACK'
    data_ret = None
    rcv_packt = None
    while True:
        if state == '0':
            rcv_packt = reveid(rcv_packt)
            if not (rcv_packt is None) and rcv_packt.corrupt(rcv_packt.msg_S):
                snd_packt = Packet.Packet(rcv_packt.ack_num + 1, NAK, '0')
                network.udt_send(snd_packt)
            elif not (rcv_packt is None) and not rcv_packt.corrupt(rcv_packt.msg_S) and rcv_packt.has_seq() == '1':
                snd_packt = Packet.Packet(rcv_packt.ack_num + 10, NAK, '0')
                network.udt_send(snd_packt)
            elif not (rcv_packt is None) and not rcv_packt.corrupt(rcv_packt.msg_S) and rcv_packt.has_seq() == '0':
                data = rcv_packt.extract()
                data_ret = deliver_data(data, data_ret)
                snd_packt = Packet.Packet(rcv_packt.ack_num + 1, ACK, '0')
                network.udt_send(snd_packt)
                state = '1'
        elif state == '1':
            if not (rcv_packt is None) and rcv_packt.corrupt(rcv_packt.msg_S):
                snd_packt = Packet.Packet(rcv_packt.ack_num + 1, NAK, '0')
                network.udt_send(snd_packt)
            elif not (rcv_packt is None) and not rcv_packt.corrupt(rcv_packt.msg_S) and rcv_packt.has_seq() == '0':
                snd_packt = Packet.Packet(rcv_packt.ack_num + 1, NAK, '0')
                network.udt_send(snd_packt)
            elif not (rcv_packt is None) and not rcv_packt.corrupt(rcv_packt.msg_S) and rcv_packt.has_seq() == '1':
                data = rcv_packt.extract()
                data_ret = deliver_data(data, data_ret)
                snd_packt = Packet.Packet(rcv_packt.ack_num + 1, ACK, '0')
                network.udt_send(snd_packt)
                state = '1'


def rdt_3_0_send(msg_S):
    pass


def rdt_3_0_receive():
    pass
