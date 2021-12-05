
import re
from Day import Day


class Day5(Day):

    def __init__(self):
        super().__init__(5)
        self.intersection_dict = {}

    def add_intersection(self, x, y):
        if (x, y) in self.intersection_dict:
            self.intersection_dict[(x, y)] += 1
        else:
            self.intersection_dict[(x, y)] = 1

    @staticmethod
    def comparator(x, y, x1, y1, x2, y2):
        if x1 < x2 and y1 < y2:
            return x <= x2 and y <= y2
        elif x1 < x2 and y2 < y1:
            return x <= x2 and y >= y2
        elif x2 < x1 and y1 < y2:
            return x >= x2 and y <= y2
        else:
            return x >= x2 and y >= y2

    @staticmethod
    def increment(x, y, x1, y1, x2, y2):
        if x1 < x2 and y1 < y2:
            return x + 1, y + 1
        elif x1 < x2 and y2 < y1:
            return x + 1, y - 1
        elif x2 < x1 and y1 < y2:
            return x - 1, y + 1
        else:
            return x - 1, y - 1

    def build_intersections(self, intersections, process_diagonal=False):
        self.intersection_dict = {}
        for line in intersections:
            data = re.split(',| -> ', line)
            x1, y1, x2, y2 = list(map(lambda i: int(i), data))
            if x1 == x2:
                for y in range(min(y1, y2), max(y1, y2)+1):
                    self.add_intersection(x1, y)
            elif y1 == y2:
                for x in range(min(x1, x2), max(x1, x2)+1):
                    self.add_intersection(x, y1)
            elif process_diagonal:
                x, y = x1, y1
                while self.comparator(x, y, x1, y1, x2, y2):
                    self.add_intersection(x, y)
                    x, y = self.increment(x, y, x1, y1, x2, y2)

    def check_intersections(self):
        return sum(1 for val in self.intersection_dict.values() if val > 1)

    def compute_intersections(self, intersections):
        self.build_intersections(intersections)
        return self.check_intersections()

    def compute_intersections_2(self, intersections):
        self.build_intersections(intersections, True)
        return self.check_intersections()

    def solution_first_star(self, input_value):
        return self.compute_intersections(input_value)

    def solution_second_star(self, input_value):
        return self.compute_intersections_2(input_value)
