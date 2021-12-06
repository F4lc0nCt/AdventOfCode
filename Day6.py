
from Day import Day


class Day6(Day):

    OLD_AGE = 6
    NEW_AGE = 8
    NB_DAY_FIRST_STAR = 80
    NB_DAY_SECOND_STAR = 256

    def __init__(self):
        super().__init__(6)

    @staticmethod
    def extract_fish_info(input_fish_string):
        return list(map(lambda x: int(x), next(input_fish_string).split(',')))

    def get_fish_grow_brute_force(self, input_fish_string, nb_day=NB_DAY_FIRST_STAR):
        input_fish = self.extract_fish_info(input_fish_string)
        for _ in range(0, nb_day):
            nb_fish_to_add = 0
            for idx in range(len(input_fish)):
                if input_fish[idx] != 0:
                    input_fish[idx] -= 1
                else:
                    input_fish[idx] = self.NEW_AGE
                    nb_fish_to_add += 1
            input_fish += [self.OLD_AGE]*nb_fish_to_add
        return len(input_fish)

    def get_fish_grow_smart(self, input_fish_string, nb_day=NB_DAY_SECOND_STAR):
        input_fish = self.extract_fish_info(input_fish_string)
        occur = {i: 0 for i in range(0, self.OLD_AGE+1)}
        for f in input_fish:
            occur[f] += 1
        for _ in range(nb_day):
            occur_tmp = {}
            for k, v in occur.items():
                if k != 0:
                    occur_tmp[k-1] = occur_tmp.setdefault(k-1, 0) + v
                else:
                    occur_tmp[self.NEW_AGE] = occur_tmp.setdefault(self.NEW_AGE, 0) + v
                    occur_tmp[self.OLD_AGE] = occur_tmp.setdefault(self.OLD_AGE, 0) + v
            occur = occur_tmp
        return sum(list(occur.values()))

    def solution_first_star(self, input_value):
        return self.get_fish_grow_brute_force(input_value)

    def solution_second_star(self, input_value):
        return self.get_fish_grow_smart(input_value)

