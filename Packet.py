# Classe do pacote



class Packet:

    def __init__(self, seq_num, msg_S, ack_num):
        self.seq_num = seq_num
        self.msg_S = msg_S
        self.ack_num = ack_num
        self.check_sum = Packet.calculate_checkSum(msg_S)
        #print(self.check_sum)

    def binarySum(a, b):
        while (b != 0):
            carry = a & b
            a = a ^ b
            b = carry << 1
        return a

    @classmethod
    def calculate_checkSum(cls, data):
        checkSum = 0
        for char in data:
            checkSum = Packet.binarySum(checkSum, ord(char))

            while (checkSum > 255):
                checkSum = checkSum % 256
                checkSum = Packet.binarySum(checkSum, 1)
        return checkSum

    def setMsg(self, msg):
        self.msg_S = msg

    def isNak(self):
        return self.msg_S == 'NAK'

    def isAck(self, seq=-1):
        if seq == -1:
            return self.msg_S == 'ACK'
        else:
            return self.msg_S == 'ACK' and self.ack_num == str(seq)

    def has_seq(self):
        return self.seq_num

    def extract(self):
        return self.msg_S

    @staticmethod
    def corrupt(msg, computed_checksum_S):
        checksum_S = Packet.calculate_checkSum(msg)
        inverted_checksum = ~computed_checksum_S & 255

        return Packet.binarySum(checksum_S, inverted_checksum) != 255
