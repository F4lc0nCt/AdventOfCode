import re
from Day import Day


class Day17(Day):

    def __init__(self):
        super().__init__(17)
        self.data_list = None
        self.data = None
        self.x_min = None
        self.x_max = None
        self.y_min = None
        self.y_max = None

    def extract_data(self, input_value):
        line = next(input_value)
        match = re.match(r'target area: x=(\d+)..(\d+), y=-?(\d+)..-?(\d+)', line)
        self.x_min = int(match.group(1))
        self.x_max = int(match.group(2))
        self.y_min = -int(match.group(3))
        self.y_max = -int(match.group(4))

    def brute_force(self, input_value):
        self.extract_data(input_value)
        higher_y = 0
        count = 0
        for x in range(0, 1000):
            for y in range(-500, 500):
                result, possible_y = self.fire(x, y)
                if result:
                    count += 1
                    higher_y = max(higher_y, possible_y)
        return count, higher_y

    def get_higher(self, input_value):
        _, y = self.brute_force(input_value)
        return y

    def get_count(self, input_value):
        count, _ = self.brute_force(input_value)
        return count

    def fire(self, x, y):
        x_pos = y_pos = 0
        x_speed = x
        y_speed = y
        higher_y = y
        while True:
            if x_pos > self.x_max or y_pos < self.y_min:
                return False, None
            if self.x_min <= x_pos <= self.x_max and \
                    self.y_min <= y_pos <= self.y_max:
                return True, higher_y
            x_pos += x_speed
            y_pos += y_speed
            higher_y = max(higher_y, y_pos)
            if x_speed > 0:
                x_speed -= 1
            elif x_speed < 0:
                x_speed += 1
            y_speed -= 1

    def solution_first_star(self, input_value):
        return self.get_higher(input_value)

    def solution_second_star(self, input_value):
        return self.get_count(input_value)
