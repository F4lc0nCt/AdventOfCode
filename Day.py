
from enum import Enum
from abc import ABC, abstractmethod
from InputParser import InputParser


class Day(ABC):

    class TestEnum(Enum):
        TEST = 0
        INPUT = 1

    class Star(Enum):
        FIRST = 1
        SECOND = 2

        def __str__(self):
            if self.value == Day.Star.FIRST.value:
                return "1st"
            else:
                return "2nd"

    class UnknownStarException(Exception):

        def __init__(self, star):
            super().__init__("Unknown Star: " + star)

    def __init__(self, day_value):
        self.day_value = day_value

    @abstractmethod
    def solution_first_star(self, input_value):
        return 0

    @abstractmethod
    def solution_second_star(self, input_value):
        return 0

    def process_first_star(self):
        self.process_star(Day.Star.FIRST)

    def process_second_star(self):
        self.process_star(Day.Star.SECOND)

    def solution_star(self, star, input_value):
        if star == Day.Star.FIRST:
            return self.solution_first_star(input_value)
        elif star == Day.Star.SECOND:
            return self.solution_second_star(input_value)
        else:
            raise Day.UnknownStarException(star)

    def process_star(self, star):
        test_case = InputParser(self.day_value, Day.TestEnum.TEST.value).get_iterator()
        test_result = self.solution_star(star, test_case)
        print(f'Day {self.day_value} - {star} star - Result Test Case is {test_result}')
        input_case = InputParser(self.day_value, Day.TestEnum.INPUT.value).get_iterator()
        input_result = self.solution_star(star, input_case)
        print(f'Day {self.day_value} - {star} star - Result Input Case is {input_result}')
