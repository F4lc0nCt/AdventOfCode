
from Day import Day


class Day1(Day):

    def __init__(self):
        super().__init__(1)

    @staticmethod
    def count_increment(depth):
        prev = int(next(depth))
        nb_increment = 0
        for elt in depth:
            if prev < int(elt):
                nb_increment += 1
            prev = int(elt)
        return nb_increment

    @staticmethod
    def count_increment_2(depth):
        current_sliding = 0
        queue = []
        for i in range(3):
            queue.append(int(next(depth)))
            current_sliding += queue[-1]
        nb_increment = 0
        for elt in depth:
            queue.append(int(elt))
            next_sliding = current_sliding + queue[-1] - queue.pop(0)
            if current_sliding < next_sliding:
                nb_increment += 1
            current_sliding = next_sliding
        return nb_increment

    def solution_first_star(self, input_value):
        return self.count_increment(input_value)

    def solution_second_star(self, input_value):
        return self.count_increment_2(input_value)

