
from Day import Day


class Day3(Day):

    def __init__(self):
        super().__init__(3)
        self.gamma = 0
        self.epsilon = 0

    def compute_consumption(self, consumptions):
        nb = 0
        nb_ones = []
        for bit in next(consumptions):
            nb_ones.append(1 if bit == "1" else 0)
        nb += 1
        for c in consumptions:
            idx = 0
            for idx in range(len(nb_ones)):
                if c[idx] == "1":
                    nb_ones[idx] += 1
            nb += 1
        gamma_string = ""
        for bit in nb_ones:
            gamma_string += "1" if 2*bit >= nb else "0"
        self.gamma = int(gamma_string, 2)
        mask = int("1"*len(nb_ones), 2)
        self.epsilon = (~self.gamma) & mask
        return self.gamma*self.epsilon

    @staticmethod
    def process_criteria(bit, consumption, is_oxy):
        nb_one = 0
        for c in consumption:
            if c[bit] == "1":
                nb_one += 1
        if is_oxy:
            keep = "1" if 2*nb_one >= len(consumption) else "0"
        else:
            keep = "0" if 2*nb_one >= len(consumption) else "1"
        idx = 0
        while idx < len(consumption):
            if consumption[idx][bit] == keep:
                idx += 1
            else:
                del consumption[idx]

    def compute_consumption_2(self, consumptions):
        oxygen_list = list(consumptions)
        co2_list = oxygen_list.copy()
        nb_bit = len(oxygen_list[0])
        bit = 0
        while (len(oxygen_list) > 1 or len(co2_list) > 1) and bit < nb_bit:
            if len(oxygen_list) > 1:
                self.process_criteria(bit, oxygen_list, True)
            if len(co2_list) > 1:
                self.process_criteria(bit, co2_list, False)
            bit += 1
        oxygen = int(oxygen_list[0], 2)
        co2 = int(co2_list[0], 2)
        return oxygen*co2

    def solution_first_star(self, input_value):
        return self.compute_consumption(input_value)

    def solution_second_star(self, input_value):
        return self.compute_consumption_2(input_value)


