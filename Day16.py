import functools
import bitstruct
from Day import Day


class Day16(Day):

    NB_BIT_PER_BYTE = 8
    OP_ID_LENGTH = 0
    OP_ID_LENGTH_NB_BYTES = 15
    OP_ID_PACKET = 1
    OP_ID_PACKET_NB_BYTES = 11
    OP_SUM = 0
    OP_MUL = 1
    OP_MIN = 2
    OP_MAX = 3
    OP_INT = 4
    OP_GREATER = 5
    OP_LESSER = 6
    OP_EQUAL = 7
    HEADER_SIZE = 6

    def __init__(self):
        super().__init__(16)
        self.data_list = None
        self.data = None

    def extract_data(self, input_value):
        self.data_list = []
        for line in input_value:
            bits = b''
            for idx in range(0, len(line), 2):
                bits += bitstruct.pack('u4u4', int(line[idx], 16), int(line[idx+1], 16))
            self.data_list.append(bits)

    def sum_version(self, input_value):
        self.extract_data(input_value)
        for idx in range(len(self.data_list)):
            self.data = self.data_list[idx]
            version, _, _ = self.process_packet(0, len(self.data)*8, None)
        return version

    def compute_data(self, input_value):
        self.extract_data(input_value)
        for idx in range(len(self.data_list)):
            self.data = self.data_list[idx]
            _, _, value = self.process_packet(0, len(self.data)*8, None)
        return value[0]

    def process_packet(self, offset, end, nb_packet):
        sum_version = 0
        idx_packet = 0
        packets = []
        while (end is None or offset < end) and (nb_packet is None or idx_packet < nb_packet):
            try:
                (version, operation) = bitstruct.unpack_from('u3u3', self.data, offset)
            except bitstruct.Error:
                break
            finally:
                offset += self.HEADER_SIZE
            sum_version += version
            if operation == self.OP_INT:
                value, offset = self.process_integer(offset)
                packets.append(value)
            else:
                offset, value, sub_version, do_break = self.process_operation(operation, offset)
                if do_break:
                    break
                packets.append(value)
                sum_version += sub_version
            idx_packet += 1
        return sum_version, offset, packets

    def process_integer(self, offset):
        total_value = 0
        eos = 1
        while eos != 0:
            (eos, value) = bitstruct.unpack_from('u1u4', self.data, offset)
            total_value = (total_value << 4) + value
            offset += 5
        return total_value, offset

    def process_operation(self, operation, offset):
        try:
            (op_id,) = bitstruct.unpack_from('u1', self.data, offset)
        except bitstruct.Error:
            return offset+1, None, None, True
        offset += 1
        if op_id == self.OP_ID_LENGTH:
            nb_bit = self.OP_ID_LENGTH_NB_BYTES
        elif op_id == self.OP_ID_PACKET:
            nb_bit = self.OP_ID_PACKET_NB_BYTES
        try:
            (total_length,) = bitstruct.unpack_from('u'+str(nb_bit), self.data, offset)
        except bitstruct.Error:
            return offset+nb_bit, None, None, True
        offset += nb_bit
        if op_id == self.OP_ID_LENGTH:
            sub_version, offset, sub_packets = self.process_packet(offset, offset + total_length, None)
        elif op_id == self.OP_ID_PACKET:
            sub_version, offset, sub_packets = self.process_packet(offset, None, total_length)
        value = self.compute_operation(operation, sub_packets)
        return offset, value, sub_version, False

    def compute_operation(self, operation, sub_packets):
        if operation == self.OP_SUM:
            return sum(sub_packets)
        elif operation == self.OP_MUL:
            return functools.reduce(lambda x, y: x*y, sub_packets)
        elif operation == self.OP_MIN:
            return min(sub_packets)
        elif operation == self.OP_MAX:
            return max(sub_packets)
        elif operation == self.OP_GREATER:
            return 1 if sub_packets[0] > sub_packets[1] else 0
        elif operation == self.OP_LESSER:
            return 1 if sub_packets[0] < sub_packets[1] else 0
        elif operation == self.OP_EQUAL:
            return 1 if sub_packets[0] == sub_packets[1] else 0

    def solution_first_star(self, input_value):
        return self.sum_version(input_value)

    def solution_second_star(self, input_value):
        return self.compute_data(input_value)
