
from Day import Day


class Day14(Day):

    NB_ITE_FIRST_STAR = 10
    NB_ITE_SECOND_STAR = 40

    def __init__(self):
        super().__init__(14)
        self.polymer = None
        self.polymer_dict = None
        self.polymer_pair = None
        self.first_letter = None
        self.last_letter = None

    def extract_data_brute_force(self, input_data):
        self.polymer = [s for s in next(input_data)]
        self.polymer_dict = {}
        next(input_data)
        for match in input_data:
            split = match.split(' -> ')
            self.polymer_dict[split[0]] = split[1]

    def run_process_brute_force(self, input_data, nb_ite):
        self.extract_data_brute_force(input_data)
        for _ in range(nb_ite):
            length = len(self.polymer)
            ite = 0
            idx = 0
            while ite < length - 1:
                new_element = self.polymer_dict[self.polymer[idx]+self.polymer[idx+1]]
                self.polymer.insert(idx+1, new_element)
                idx += 2
                ite += 1
        return self.count_element_brute_force()

    def count_element_brute_force(self):
        count_dict = {}
        for e in self.polymer:
            count_dict[e] = count_dict.get(e, 0) + 1
        maxi = mini = None
        for _, v in count_dict.items():
            if maxi is None or maxi < v:
                maxi = v
            if mini is None or mini > v:
                mini = v
        return maxi-mini

    def extract_data(self, input_data):
        s = next(input_data)
        self.polymer_pair = {}
        self.first_letter = s[0]
        self.last_letter = s[-1]
        for i in range(len(s)-1):
            pair = s[i]+s[i+1]
            self.polymer_pair[pair] = self.polymer_pair.get(pair, 0) + 1
        self.polymer_dict = {}
        next(input_data)
        for match in input_data:
            split = match.split(' -> ')
            self.polymer_dict[split[0]] = split[1]

    def run_process(self, input_data, nb_ite):
        self.extract_data(input_data)
        for _ in range(nb_ite):
            tmp_dict = {}
            for k, v in self.polymer_pair.items():
                fst = k[0]+self.polymer_dict[k]
                snd = self.polymer_dict[k]+k[1]
                tmp_dict[fst] = tmp_dict.get(fst, 0) + v
                tmp_dict[snd] = tmp_dict.get(snd, 0) + v
            self.polymer_pair = tmp_dict
        return self.count_element()

    def build_count_dict(self):
        count_dict = {}
        for e, v in self.polymer_pair.items():
            count_dict[e[0]] = count_dict.get(e[0], 0) + v
            count_dict[e[1]] = count_dict.get(e[1], 0) + v
        return count_dict

    def count_element(self):
        count_dict = self.build_count_dict()
        maxi = mini = None
        for k, v in count_dict.items():
            if (k == self.first_letter and k != self.last_letter) or \
                    (k != self.first_letter and k == self.last_letter):
                count_dict[k] = (v - 1)//2 + 1
            elif k == self.first_letter and k == self.last_letter:
                count_dict[k] = v//2 + 1
            else:
                count_dict[k] = v//2
            new_v = count_dict[k]
            if maxi is None or maxi < new_v:
                maxi = new_v
            if mini is None or mini > new_v:
                mini = new_v
        return maxi-mini

    def solution_first_star(self, input_value):
        return self.run_process(input_value, self.NB_ITE_FIRST_STAR)

    def solution_second_star(self, input_value):
        return self.run_process(input_value, self.NB_ITE_SECOND_STAR)
