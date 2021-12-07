
from Day import Day


class Day7(Day):

    def __init__(self):
        super().__init__(7)

    @staticmethod
    def extract_fish_info(input_fish_string):
        return list(map(lambda x: int(x), next(input_fish_string).split(',')))

    @staticmethod
    def consume_linear_fuel(start, end):
        return abs(end-start)

    @staticmethod
    def consume_incremental_fuel(start, end):
        dist = abs(end-start)
        return dist * (dist + 1) // 2

    @staticmethod
    def get_crab_position(crab_position_string):
        return list(map(lambda x: int(x), next(crab_position_string).split(',')))

    def find_crab_center(self, crab_position_string, consume_fuel_method):
        crab_position = self.get_crab_position(crab_position_string)
        min_dist = None
        for center in range(min(crab_position), max(crab_position) + 1):
            current_dist = 0
            for position in crab_position:
                current_dist += consume_fuel_method(position, center)
            if min_dist is None or current_dist < min_dist:
                min_dist = current_dist
        return min_dist

    def solution_first_star(self, input_value):
        return self.find_crab_center(input_value, self.consume_linear_fuel)

    def solution_second_star(self, input_value):
        return self.find_crab_center(input_value, self.consume_incremental_fuel)

