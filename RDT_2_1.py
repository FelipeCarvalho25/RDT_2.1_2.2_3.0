# Esta é a camada de transporte
import network
import timer
import Packet
import time
import host_a
import host_b
from queue import Queue


def reveid(queue):
    return network.receivd(queue)


def deliver_data(msg):
    host_b.to_app_layer(msg)


def rdt_2_1_send(msg_S, queue_a, queue_b ):
    state = '0'
    rcv_packt = None
    cont = 0
    while True:
        cont += 1
        if cont == 50000000:
            break
        if state == '0':
            snd_packt = Packet.Packet(0, msg_S, '0')
            # if RDT_2_1.send_ready(msg_S):
            network.udt_send(snd_packt, queue_b, 10)
             
            state = '1'
        elif state == '1':
            snd_packt = Packet.Packet(0, msg_S, '0')
            rcv_packt = reveid(queue_a)
            # 
            if not (rcv_packt is None) and (
                    rcv_packt.corrupt(rcv_packt.msg_S, rcv_packt.check_sum) or rcv_packt.isNak()):
                network.udt_send(snd_packt, queue_b, 10)
                 
            elif not (rcv_packt is None) and not rcv_packt.corrupt(rcv_packt.msg_S,
                                                                   rcv_packt.check_sum) and rcv_packt.isAck():
                state = '2'
        elif state == '2':
            snd_packt = Packet.Packet(1, msg_S, '1')
            network.udt_send(snd_packt, queue_b, 10)
             
            state = '3'
        elif state == '3':
            snd_packt = Packet.Packet(1, msg_S, '1')
            rcv_packt = reveid(queue_a)
            # 
            if not (rcv_packt is None) and (
                    rcv_packt.corrupt(rcv_packt.msg_S, rcv_packt.check_sum) or rcv_packt.isNak()):
                network.udt_send(snd_packt, queue_b, 10)
                 
            elif not (rcv_packt is None) and not rcv_packt.corrupt(rcv_packt.msg_S,
                                                                   rcv_packt.check_sum) and rcv_packt.isAck():
                state = '1'


def rdt_2_1_receive(queue_a, queue_b ):
    state = '0'
    NAK = 'NAK'
    ACK = 'ACK'
    cont = 0
    while True:
        cont += 1
        if cont == 5000:
            break
        if state == '0':
            rcv_packt = reveid(queue_b)
            # 
            if not (rcv_packt is None) and rcv_packt.corrupt(rcv_packt.msg_S, rcv_packt.check_sum):
                snd_packt = Packet.Packet(rcv_packt.seq_num, NAK, '0')
                network.udt_send(snd_packt, queue_a, 5)
                 
            elif not (rcv_packt is None) and not rcv_packt.corrupt(rcv_packt.msg_S,
                                                                   rcv_packt.check_sum) and rcv_packt.has_seq() == 1:
                snd_packt = Packet.Packet(rcv_packt.seq_num, ACK, '1')
                network.udt_send(snd_packt, queue_a, 5)
                 
            elif not (rcv_packt is None) and not rcv_packt.corrupt(rcv_packt.msg_S,
                                                                   rcv_packt.check_sum) and rcv_packt.has_seq() == 0:
                data = rcv_packt.extract()
                deliver_data(data)
                snd_packt = Packet.Packet(rcv_packt.seq_num, ACK, '0')
                network.udt_send(snd_packt, queue_a, 5)
                 
                state = '1'
        elif state == '1':
            rcv_packt = reveid(queue_b)
            # 
            if not (rcv_packt is None) and rcv_packt.corrupt(rcv_packt.msg_S, rcv_packt.check_sum):
                snd_packt = Packet.Packet(rcv_packt.seq_num, NAK, '1')
                network.udt_send(snd_packt, queue_a, 5)
                 
            elif not (rcv_packt is None) and not rcv_packt.corrupt(rcv_packt.msg_S,
                                                                   rcv_packt.check_sum) and rcv_packt.has_seq() == 0:
                snd_packt = Packet.Packet(rcv_packt.seq_num, ACK, '0')
                network.udt_send(snd_packt, queue_a, 5)
                 
            elif not (rcv_packt is None) and not rcv_packt.corrupt(rcv_packt.msg_S,
                                                                   rcv_packt.check_sum) and rcv_packt.has_seq() == 1:
                data = rcv_packt.extract()
                deliver_data(data)
                snd_packt = Packet.Packet(rcv_packt.seq_num, ACK, '1')
                network.udt_send(snd_packt, queue_a, 5)
                 
                state = '1'


def rdt_2_2_send(msg_S, queue_a, queue_b ):
    state = '0'
    rcv_packt = None
    cont = 0
    while True:
        cont += 1
        if cont == 5000:
            break
        if state == '0':
            snd_packt = Packet.Packet(0, msg_S, '0')
            # if RDT_2_1.send_ready(msg_S):
            network.udt_send(snd_packt, queue_b, 15)
             
            state = '1'
        elif state == '1':
            snd_packt = Packet.Packet(0, msg_S, '0')
            rcv_packt = reveid(queue_a)
            # 
            if not (rcv_packt is None) and (
                    rcv_packt.corrupt(rcv_packt.msg_S, rcv_packt.check_sum) or rcv_packt.isAck(1)):
                network.udt_send(snd_packt, queue_b, 15)
                 
            elif not (rcv_packt is None) and not rcv_packt.corrupt(rcv_packt.msg_S,
                                                                   rcv_packt.check_sum) and rcv_packt.isAck(0):
                state = '2'
        elif state == '2':
            snd_packt = Packet.Packet(1, msg_S, '1')
            network.udt_send(snd_packt, queue_b, 15)
             
            state = '3'
        elif state == '3':
            snd_packt = Packet.Packet(1, msg_S, '1')
            rcv_packt = reveid(queue_a)
            # 
            if not (rcv_packt is None) and (
                    rcv_packt.corrupt(rcv_packt.msg_S, rcv_packt.check_sum) or rcv_packt.isAck(0)):
                network.udt_send(snd_packt, queue_b, 15)
                 
            elif not (rcv_packt is None) and not rcv_packt.corrupt(rcv_packt.msg_S,
                                                                   rcv_packt.check_sum) and rcv_packt.isAck(1):
                state = '1'


def rdt_2_2_receive(queue_a, queue_b ):
    state = '0'
    NAK = 'NAK'
    ACK = 'ACK'
    cont = 0
    while True:
        cont += 1
        if cont == 5000:
            break
        if state == '0':
            rcv_packt = reveid(queue_b)
            # 
            if not (rcv_packt is None) and (
                    rcv_packt.corrupt(rcv_packt.msg_S, rcv_packt.check_sum) or rcv_packt.has_seq() == 1):
                snd_packt = Packet.Packet(rcv_packt.seq_num, ACK, '1')
                network.udt_send(snd_packt, queue_a, 5)
                 
            elif not (rcv_packt is None) and not rcv_packt.corrupt(rcv_packt.msg_S,
                                                                   rcv_packt.check_sum) and rcv_packt.has_seq() == 0:
                data = rcv_packt.extract()
                deliver_data(data)
                snd_packt = Packet.Packet(rcv_packt.seq_num, ACK, '0')
                network.udt_send(snd_packt, queue_a, 5)
                 
                state = '1'
        elif state == '1':
            rcv_packt = reveid(queue_b)
            # 
            if not (rcv_packt is None) and (rcv_packt.corrupt(rcv_packt.msg_S,
                                                              rcv_packt.check_sum) or rcv_packt.has_seq() == 0):
                snd_packt = Packet.Packet(rcv_packt.seq_num, ACK, '0')
                network.udt_send(snd_packt, queue_a, 5)
                 
            elif not (rcv_packt is None) and not rcv_packt.corrupt(rcv_packt.msg_S,
                                                                   rcv_packt.check_sum) and rcv_packt.has_seq() == 1:
                data = rcv_packt.extract()
                deliver_data(data)
                snd_packt = Packet.Packet(rcv_packt.seq_num, ACK, '1')
                network.udt_send(snd_packt, queue_a, 5)
                 
                state = '1'


def rdt_3_0_send(msg_S, queue_a, queue_b ):
    state = '0'
    rcv_packt = None
    rdt_timer = 0
    cont = 0
    while True:
        cont += 1
        if cont == 5000:
            break
        if state == '0':
            snd_packt = Packet.Packet(0, msg_S, '0')

            # if RDT_2_1.send_ready(msg_S):
            network.udt_send(snd_packt, queue_b, 20)
             
            timer.start_timer(rdt_timer)
            state = '1'

        elif state == '1':
            snd_packt = Packet.Packet(0, msg_S, '0')
            rcv_packt = reveid(queue_a)
            # 

            if timer.timeout(rdt_timer):
                network.udt_send(snd_packt, queue_b, 20)
                 
                timer.start_timer(rdt_timer)

            elif not (rcv_packt is None) and not rcv_packt.corrupt(rcv_packt.msg_S, rcv_packt.check_sum) and rcv_packt.isNak():
                state = '2'

        elif state == '2':
            snd_packt = Packet.Packet(1, msg_S, '1')
            rcv_packt = reveid(queue_a)
            # 

            # elif RDT_2_1.send_ready(msg_S):
            network.udt_send(snd_packt, queue_b, 20)
             
            timer.start_timer(rdt_timer)
            state = '3'

        elif state == '3':
            snd_packt = Packet.Packet(0, msg_S, '1')
            rcv_packt = reveid(queue_a)
            # 

            if timer.timeout(rdt_timer):
                network.udt_send(snd_packt, queue_b, 20)
                 
                timer.start_timer(rdt_timer)

            elif not (rcv_packt is None) and not rcv_packt.corrupt(rcv_packt.msg_S, rcv_packt.check_sum) and rcv_packt.isAck():
                state = '1'

def rdt_3_0_receive(queue_a, queue_b ):
    state = '0'
    NAK = 'NAK'
    ACK = 'ACK'
    cont = 0
    while True:
        cont += 1
        if cont == 5000:
            break
        if state == '0':
            rcv_packt = reveid(queue_b)
            # 

            if not (rcv_packt is None) and (rcv_packt.corrupt(rcv_packt.msg_S, rcv_packt.check_sum) or rcv_packt.has_seq() == 1):
                snd_packt = Packet.Packet(rcv_packt.seq_num, ACK, '1')
                network.udt_send(snd_packt, queue_a, 20, 15)
                 

            elif not (rcv_packt is None) and not rcv_packt.corrupt(rcv_packt.msg_S, rcv_packt.check_sum) and rcv_packt.has_seq() == 0:
                data = rcv_packt.extract()
                deliver_data(data)
                snd_packt = Packet.Packet(rcv_packt.seq_num, ACK, '0')
                network.udt_send(snd_packt, queue_a, 20, 15)
                 
                state = '1'

        elif state == '1':
            rcv_packt = reveid(queue_b)
            # 

            if not (rcv_packt is None) and (rcv_packt.corrupt(rcv_packt.msg_S, rcv_packt.check_sum) or rcv_packt.has_seq() == 0):
                snd_packt = Packet.Packet(rcv_packt.seq_num, ACK, '0')
                network.udt_send(snd_packt, queue_a, 20, 15)
                 

            elif not (rcv_packt is None) and not rcv_packt.corrupt(rcv_packt.msg_S, rcv_packt.check_sum) and rcv_packt.has_seq() == 1:
                data = rcv_packt.extract()
                deliver_data(data)
                snd_packt = Packet.Packet(rcv_packt.seq_num, ACK, '1')
                network.udt_send(snd_packt, queue_a, 20, 15)
                 
                state = '1'
