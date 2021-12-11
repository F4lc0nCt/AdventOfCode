
import bisect
from Day import Day


class Day10(Day):

    MATCH = {')': '(', '>': '<', '}': '{', ']': '['}
    MATCH_REV = {'(': ')', '<': '>', '{': '}', '[': ']'}
    POINTS = {')': 3, ']': 57, '}': 1197, '>': 25137}
    COMPLETE_PTS = {')': 1, ']': 2, '}': 3, '>': 4}

    def __init__(self):
        super().__init__(10)

    def find_corrupted_line(self, input_data):
        count = 0
        for line in input_data:
            value, _ = self.process_line(line)
            count += value
        return count

    def fill_incomplete_line(self, input_data):
        scores = []
        for line in input_data:
            value, stack = self.process_line(line)
            if value == 0 and len(stack) > 0:
                bisect.insort(scores, self.complete_line(stack))
        return scores[len(scores)//2]

    def process_line(self, line):
        stack = []
        for e in line:
            if e in self.MATCH.values():
                stack.append(e)
            else:
                if len(stack) == 0 or stack.pop() != self.MATCH[e]:
                    return self.POINTS[e], None
        return 0, stack

    def complete_line(self, stack):
        count = 0
        while len(stack) > 0:
            count *= 5
            count += self.COMPLETE_PTS[self.MATCH_REV[stack.pop()]]
        return count

    def solution_first_star(self, input_value):
        return self.find_corrupted_line(input_value)

    def solution_second_star(self, input_value):
        return self.fill_incomplete_line(input_value)

