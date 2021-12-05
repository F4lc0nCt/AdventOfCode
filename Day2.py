
from enum import Enum
from Day import Day


class Day2(Day):

    class Direction(Enum):
        FORWARD = "forward"
        DOWN = "down"
        UP = "up"

    def __init__(self):
        super().__init__(2)
        self.x = 0
        self.y = 0
        self.aim = 0

    class UnknownDirection(Exception):

        def __init__(self, direction):
            super().__init__("Unknown direction: " + direction)

    def process_direction(self, direction, value):
        if direction == Day2.Direction.FORWARD.value:
            self.x += value
        elif direction == Day2.Direction.DOWN.value:
            self.y += value
        elif direction == Day2.Direction.UP.value:
            self.y -= value
        else:
            raise Day2.UnknownDirection(direction)

    def get_position(self, order):
        self.x = 0
        self.y = 0
        self.aim = 0
        for elt in order:
            split_order = elt.split(" ")
            direction = split_order[0]
            value = int(split_order[1])
            self.process_direction(direction, value)
        return self.x * self.y

    def process_direction_2(self, direction, value):
        if direction == Day2.Direction.FORWARD.value:
            self.x += value
            self.y += self.aim*value
        elif direction == Day2.Direction.DOWN.value:
            self.aim += value
        elif direction == Day2.Direction.UP.value:
            self.aim -= value
        else:
            raise Day2.UnknownDirection(direction)

    def get_position_2(self, order):
        self.x = 0
        self.y = 0
        self.aim = 0
        for elt in order:
            split_order = elt.split(" ")
            direction = split_order[0]
            value = int(split_order[1])
            self.process_direction_2(direction, value)
        return self.x * self.y

    def solution_first_star(self, input_value):
        return self.get_position(input_value)

    def solution_second_star(self, input_value):
        return self.get_position_2(input_value)


