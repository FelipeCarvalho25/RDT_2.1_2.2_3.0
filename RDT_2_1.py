# Esta é a camada de transporte
import network
import timer
import Packet
import host_b


def reveid(queue):
    return network.udt_receivd(queue)


def deliver_data(msg):
    host_b.to_app_layer(msg)


def rdt_2_1_send(msg_S, queue_a, queue_b):
    state = '0'
    completed_ciclo = False
    cont = 0
    posMsg = 0
    n = int(len(msg_S) / 10)
    splited = []
    if n > 1:
        len_l = len(msg_S)
        for i in range(n):
            start = int(i * len_l / n)
            end = int((i + 1) * len_l / n)
            splited.append(msg_S[start:end])
    while True:
        cont += 1
        if cont == 50000000:
            break
        if 1 < n > posMsg:
            msg_S = splited[posMsg]

        if 1 < n <= posMsg or (completed_ciclo and n == 1):
            print("Finalizado envio de mensagens")
            break
        if state == '0':
            completed_ciclo = False
            snd_packt = Packet.Packet(0, msg_S, '0')
            print("HOST A - Enviando Mensagem 0")
            network.udt_send(snd_packt, queue_b, 10)
            state = '1'
        elif state == '1':
            snd_packt = Packet.Packet(0, msg_S, '0')
            rcv_packt = reveid(queue_a)
            if not (rcv_packt is None) and (
                    rcv_packt.corrupt(rcv_packt.msg_S, rcv_packt.check_sum) or rcv_packt.isNak()):
                print("HOST A - Reenviando Mensagem 0")
                network.udt_send(snd_packt, queue_b, 10)

            elif not (rcv_packt is None) and not rcv_packt.corrupt(rcv_packt.msg_S,
                                                                   rcv_packt.check_sum) and rcv_packt.isAck():
                state = '2'
                if n > 1:
                    posMsg += 1
        elif state == '2':
            snd_packt = Packet.Packet(1, msg_S, '1')
            print("HOST A - Enviando Mensagem 1")
            network.udt_send(snd_packt, queue_b, 10)
            state = '3'
        elif state == '3':
            snd_packt = Packet.Packet(1, msg_S, '1')
            rcv_packt = reveid(queue_a)
            #
            if not (rcv_packt is None) and (
                    rcv_packt.corrupt(rcv_packt.msg_S, rcv_packt.check_sum) or rcv_packt.isNak()):
                print("HOST A - Reenviando Mensagem")
                network.udt_send(snd_packt, queue_b, 10)

            elif not (rcv_packt is None) and not rcv_packt.corrupt(rcv_packt.msg_S,
                                                                   rcv_packt.check_sum) and rcv_packt.isAck():
                state = '0'
                completed_ciclo = True
                if n > 1:
                    posMsg += 1


def rdt_2_1_receive(queue_a, queue_b):
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
            if not (rcv_packt is None) and rcv_packt.corrupt(rcv_packt.msg_S, rcv_packt.check_sum):
                snd_packt = Packet.Packet(rcv_packt.seq_num, NAK, '0')
                print("HOST B - Enviando NAK 0")
                network.udt_send(snd_packt, queue_a, 5)

            elif not (rcv_packt is None) and not rcv_packt.corrupt(rcv_packt.msg_S,
                                                                   rcv_packt.check_sum) and rcv_packt.has_seq() == 1:
                snd_packt = Packet.Packet(rcv_packt.seq_num, ACK, '1')
                print("HOST B - Enviando ACK 1")
                network.udt_send(snd_packt, queue_a, 5)

            elif not (rcv_packt is None) and not rcv_packt.corrupt(rcv_packt.msg_S,
                                                                   rcv_packt.check_sum) and rcv_packt.has_seq() == 0:
                data = rcv_packt.extract()
                deliver_data(data)
                print("HOST B - Enviando ACK 0")
                snd_packt = Packet.Packet(rcv_packt.seq_num, ACK, '0')
                network.udt_send(snd_packt, queue_a, 5)
                state = '1'
        elif state == '1':
            rcv_packt = reveid(queue_b)
            # print("buscou pacote")
            if not (rcv_packt is None) and rcv_packt.corrupt(rcv_packt.msg_S, rcv_packt.check_sum):
                print("HOST B - Enviando NAK 1")
                snd_packt = Packet.Packet(rcv_packt.seq_num, NAK, '1')
                network.udt_send(snd_packt, queue_a, 5)

            elif not (rcv_packt is None) and not rcv_packt.corrupt(rcv_packt.msg_S,
                                                                   rcv_packt.check_sum) and rcv_packt.has_seq() == 0:
                print("HOST B - Enviando ACK 0")
                snd_packt = Packet.Packet(rcv_packt.seq_num, ACK, '0')
                network.udt_send(snd_packt, queue_a, 5)

            elif not (rcv_packt is None) and not rcv_packt.corrupt(rcv_packt.msg_S,
                                                                   rcv_packt.check_sum) and rcv_packt.has_seq() == 1:
                print("HOST B - Enviando ACK 1")
                data = rcv_packt.extract()
                deliver_data(data)
                snd_packt = Packet.Packet(rcv_packt.seq_num, ACK, '1')
                network.udt_send(snd_packt, queue_a, 5)
                state = '0'
            else:
                cont -= 1


def rdt_2_2_send(msg_S, queue_a, queue_b):
    state = '0'
    completed_ciclo = False
    cont = 0
    posMsg = 0
    n = int(len(msg_S) / 10)
    splited = []
    if n > 1:
        len_l = len(msg_S)
        for i in range(n):
            start = int(i * len_l / n)
            end = int((i + 1) * len_l / n)
            splited.append(msg_S[start:end])
    while True:
        cont += 1
        if cont == 5000:
            break
        if 1 < n > posMsg:
            msg_S = splited[posMsg]
        if 1 < n <= posMsg or (completed_ciclo and n == 1):
            print("Finalizado envio de mensagens")
            break
        if state == '0':
            snd_packt = Packet.Packet(0, msg_S, '0')
            print("HOST A - Enviando Mensagem 0")
            network.udt_send(snd_packt, queue_b, 15)
            state = '1'
        elif state == '1':
            snd_packt = Packet.Packet(0, msg_S, '0')
            rcv_packt = reveid(queue_a)
            if not (rcv_packt is None) and (
                    rcv_packt.corrupt(rcv_packt.msg_S, rcv_packt.check_sum) or rcv_packt.isAck(1)):
                    print("HOST A - Reenviando Mensagem 0")
                    network.udt_send(snd_packt, queue_b, 15)

            elif not (rcv_packt is None) and not rcv_packt.corrupt(rcv_packt.msg_S,
                                                                   rcv_packt.check_sum) and rcv_packt.isAck(0):
                state = '2'
                if n > 1:
                    posMsg += 1
        elif state == '2':
            snd_packt = Packet.Packet(1, msg_S, '1')
            print("HOST A - Enviando Mensagem 1")
            network.udt_send(snd_packt, queue_b, 15)
            state = '3'
        elif state == '3':
            snd_packt = Packet.Packet(1, msg_S, '1')
            rcv_packt = reveid(queue_a)
            if not (rcv_packt is None) and (
                    rcv_packt.corrupt(rcv_packt.msg_S, rcv_packt.check_sum) or rcv_packt.isAck(0)):
                print("HOST A - Reenviando Mensagem 1")
                network.udt_send(snd_packt, queue_b, 15)

            elif not (rcv_packt is None) and not rcv_packt.corrupt(rcv_packt.msg_S,
                                                                   rcv_packt.check_sum) and rcv_packt.isAck(1):
                state = '0'
                completed_ciclo = True
                if n > 1:
                    posMsg += 1


def rdt_2_2_receive(queue_a, queue_b):
    state = '0'
    ACK = 'ACK'
    cont = 0
    while True:
        cont += 1
        if cont == 5000:
            break
        if state == '0':
            rcv_packt = reveid(queue_b)
            if not (rcv_packt is None) and (
                    rcv_packt.corrupt(rcv_packt.msg_S, rcv_packt.check_sum) or rcv_packt.has_seq() == 1):
                snd_packt = Packet.Packet(rcv_packt.seq_num, ACK, '1')
                print("HOST B - Enviando ACK 1")
                network.udt_send(snd_packt, queue_a, 5)

            elif not (rcv_packt is None) and not rcv_packt.corrupt(rcv_packt.msg_S,
                                                                   rcv_packt.check_sum) and rcv_packt.has_seq() == 0:
                data = rcv_packt.extract()
                deliver_data(data)
                snd_packt = Packet.Packet(rcv_packt.seq_num, ACK, '0')
                print("HOST B - Enviando ACK 0")
                network.udt_send(snd_packt, queue_a, 5)
                state = '1'
        elif state == '1':
            rcv_packt = reveid(queue_b)
            if not (rcv_packt is None) and (rcv_packt.corrupt(rcv_packt.msg_S,
                                                              rcv_packt.check_sum) or rcv_packt.has_seq() == 0):
                snd_packt = Packet.Packet(rcv_packt.seq_num, ACK, '0')
                print("HOST B - Enviando ACK 0")
                network.udt_send(snd_packt, queue_a, 5)
            elif not (rcv_packt is None) and not rcv_packt.corrupt(rcv_packt.msg_S,
                                                                   rcv_packt.check_sum) and rcv_packt.has_seq() == 1:
                data = rcv_packt.extract()
                deliver_data(data)
                snd_packt = Packet.Packet(rcv_packt.seq_num, ACK, '1')
                print("HOST B - Enviando ACK 1")
                network.udt_send(snd_packt, queue_a, 5)
                state = '0'


def rdt_3_0_send(msg_S, queue_a, queue_b):
    rdt_timer = 0
    state = '0'
    completed_ciclo = False
    cont = 0
    posMsg = 0
    n = int(len(msg_S) / 10)
    splited = []
    if n > 1:
        len_l = len(msg_S)
        for i in range(n):
            start = int(i * len_l / n)
            end = int((i + 1) * len_l / n)
            splited.append(msg_S[start:end])
    while True:
        cont += 1
        if cont == 5000:
            break
        if 1 < n > posMsg:
            msg_S = splited[posMsg]

        if 1 < n <= posMsg or (completed_ciclo and n == 1):
            print("Finalizado envio de mensagens")
            break
        if state == '0':
            snd_packt = Packet.Packet(0, msg_S, '0')
            print("HOST A - Enviando mensagem 0")
            network.udt_send(snd_packt, queue_b, 20)
            timer.start_timer(rdt_timer)
            state = '1'
        elif state == '1':
            snd_packt = Packet.Packet(0, msg_S, '0')
            rcv_packt = reveid(queue_a)
            if timer.timeout(rdt_timer):
                print("HOST A - Reenviando mensagem 0")
                network.udt_send(snd_packt, queue_b, 20)
                timer.start_timer(rdt_timer)
            elif not (rcv_packt is None) and not rcv_packt.corrupt(rcv_packt.msg_S,
                                                                   rcv_packt.check_sum) and rcv_packt.isNak():
                state = '2'
                if n > 1:
                    posMsg += 1

        elif state == '2':
            snd_packt = Packet.Packet(1, msg_S, '1')
            print("HOST A - Enviando mensagem 1")
            network.udt_send(snd_packt, queue_b, 20)
            timer.start_timer(rdt_timer)
            state = '3'
        elif state == '3':
            snd_packt = Packet.Packet(1, msg_S, '1')
            rcv_packt = reveid(queue_a)
            if timer.timeout(rdt_timer):
                print("HOST A - Reenviando mensagem 1")
                network.udt_send(snd_packt, queue_b, 20)
                timer.start_timer(rdt_timer)
            elif not (rcv_packt is None) and not rcv_packt.corrupt(rcv_packt.msg_S,
                                                                   rcv_packt.check_sum) and rcv_packt.isAck():
                state = '0'
                completed_ciclo = True
                if n > 1:
                    posMsg += 1


def rdt_3_0_receive(queue_a, queue_b):
    state = '0'
    ACK = 'ACK'
    cont = 0
    while True:
        cont += 1
        if cont == 5000:
            break
        if state == '0':
            rcv_packt = reveid(queue_b)
            if not (rcv_packt is None) and (
                    rcv_packt.corrupt(rcv_packt.msg_S, rcv_packt.check_sum) or rcv_packt.has_seq() == 1):
                snd_packt = Packet.Packet(rcv_packt.seq_num, ACK, '1')
                print("HOST B - Enviando ACK 1")
                network.udt_send(snd_packt, queue_a, 25, 15)
            elif not (rcv_packt is None) and not rcv_packt.corrupt(rcv_packt.msg_S,
                                                                   rcv_packt.check_sum) and rcv_packt.has_seq() == 0:
                data = rcv_packt.extract()
                deliver_data(data)
                snd_packt = Packet.Packet(rcv_packt.seq_num, ACK, '0')
                network.udt_send(snd_packt, queue_a, 25, 15)
                state = '1'
                print("HOST B - Enviando ACK 0")
        elif state == '1':
            rcv_packt = reveid(queue_b)
            if not (rcv_packt is None) and (
                    rcv_packt.corrupt(rcv_packt.msg_S, rcv_packt.check_sum) or rcv_packt.has_seq() == 0):
                snd_packt = Packet.Packet(rcv_packt.seq_num, ACK, '0')
                network.udt_send(snd_packt, queue_a, 25, 15)
                print("HOST B - Enviando ACK 0")
            elif not (rcv_packt is None) and not rcv_packt.corrupt(rcv_packt.msg_S,
                                                                   rcv_packt.check_sum) and rcv_packt.has_seq() == 1:
                data = rcv_packt.extract()
                deliver_data(data)
                snd_packt = Packet.Packet(rcv_packt.seq_num, ACK, '1')
                network.udt_send(snd_packt, queue_a, 25, 15)
                state = '0'
                print("HOST B - Enviando ACK 1")
