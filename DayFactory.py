
from Day1 import Day1
from Day2 import Day2
from Day3 import Day3
from Day4 import Day4
from Day5 import Day5


class DayFactory:

    def __init__(self, max_day):
        self.max_day = max_day
        pass

    def get_day(self, day_value):
        if day_value > self.max_day:
            raise Exception(f'Problem not posted yet. '
                            f'Max is {self.max_day}.'
                            f'Requested day is {day_value}')
        print(f'Working on day {day_value}')
        if day_value == 1:
            return Day1()
        elif day_value == 2:
            return Day2()
        elif day_value == 3:
            return Day3()
        elif day_value == 4:
            return Day4()
        elif day_value == 5:
            return Day5()
        else:
            raise Exception("Unknown day value: "+ day_value)

