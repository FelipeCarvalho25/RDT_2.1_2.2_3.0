# Classe do pacote
import hashlib


class Packet:

    def __init__(self, seq_num, msg_S, ack_num):
        self.seq_num = seq_num
        self.msg_S = msg_S
        self.ack_num = ack_num
        self.check_sum = Packet.calculate_checkSum(msg_S)

    @classmethod
    def calculate_checkSum(cls, data):
        checkSum = 1
        return checkSum

    def isNak(self):
        return self.msg_S == 'NAK'

    def isAck(self):
        return self.msg_S == 'ACK'

    def has_seq(self):
        return self.seq_num

    def extract(self):
        return self.msg_S

    @staticmethod
    def corrupt(msg, computed_checksum_S):
        # extract the fields
        checksum_S = Packet.calculate_checkSum(msg)
        # and check if the same
        return checksum_S != computed_checksum_S
