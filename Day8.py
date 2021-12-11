from typing import Set

from Day import Day


class Day8(Day):
    LEN_GUESS = {2: {1},
                 3: {7},
                 4: {4},
                 5: {2, 3, 5},
                 6: {0, 6, 9},
                 7: {8}}

    MATCH_NB = {'abcefg': 0, 'cf': 1, 'acdeg': 2, 'acdfg': 3, 'bcdf': 4, 'abdfg': 5, 'abdefg': 6,
                'acf': 7, 'abcdefg': 8, 'abcdfg': 9}

    def __init__(self):
        super().__init__(8)
        self.patterns = None
        self.combinations = None
        self.combinations_nb = None
        self.guesses = None

    def build_data(self, input_data):
        self.patterns = []
        self.combinations = []
        self.guesses = []
        for line in input_data:
            line_split = line.split(' | ')
            self.patterns.append(line_split[0].split(' '))
            self.combinations.append((line_split[1].split(' ')))

    def count_easy_guesses(self, input_data):
        self.build_data(input_data)
        count = 0
        for c in self.combinations:
            for digit in c:
                if 1 < len(digit) < 5 or len(digit) == 7:
                    count += 1
        return count

    @staticmethod
    def revert_combination(guess):
        mapping = {}
        one = four = seven = None
        all_char = {'a', 'b', 'c', 'd', 'e', 'f', 'g'}
        var_069 = set()
        for key in guess:
            if len(key) == 2:
                one = set([c for c in key])
            elif len(key) == 3:
                seven = set([c for c in key])
            elif len(key) == 4:
                four = set([c for c in key])
            elif len(key) == 6:
                var_069 = var_069.union(all_char.difference(key))
        revert_a = seven.difference(one).pop()
        revert_bd = four.difference(one)
        revert_c = var_069.intersection(one).pop()
        revert_d = revert_bd.intersection(var_069).pop()
        revert_b = revert_bd.difference({revert_d}).pop()
        revert_f = one.difference({revert_c}).pop()
        revert_e = var_069.difference({revert_c, revert_d}).pop()
        revert_g = all_char.difference({revert_a, revert_b, revert_c, revert_d, revert_e, revert_f}).pop()
        mapping[revert_a] = 'a'
        mapping[revert_b] = 'b'
        mapping[revert_c] = 'c'
        mapping[revert_d] = 'd'
        mapping[revert_e] = 'e'
        mapping[revert_f] = 'f'
        mapping[revert_g] = 'g'
        return mapping

    def find_combination(self, input_value):
        self.build_data(input_value)
        self.guesses = []
        self.combinations_nb = []
        for idx in range(len(self.patterns)):
            guess = {i: self.LEN_GUESS[len(i)] for i in self.patterns[idx]}
            mapping = self.revert_combination(guess)
            self.combinations_nb.append([])
            for i in range(len(self.combinations[idx])):
                tmp = []
                for j in range(len(self.combinations[idx][i])):
                    tmp.append(mapping[self.combinations[idx][i][j]])
                tmp.sort()
                tmp_str = ""
                for letter in tmp:
                    tmp_str += letter
                self.combinations_nb[-1].append(self.MATCH_NB[tmp_str])
            value = 0
            start = 1000
            for elt in self.combinations_nb[-1]:
                value += elt*start
                start = start // 10
            self.combinations_nb[-1] = value
        return sum(self.combinations_nb)

    def solution_first_star(self, input_value):
        return self.count_easy_guesses(input_value)

    def solution_second_star(self, input_value):
        return self.find_combination(input_value)
