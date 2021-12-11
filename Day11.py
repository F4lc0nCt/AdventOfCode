
from Day import Day


class Day11(Day):

    def __init__(self):
        super().__init__(11)
        self.octopuses = None
        self.n = None
        self.m = None

    def extract_data(self, input_data):
        self.octopuses = []
        self.n = self.m = 0
        for line in input_data:
            self.octopuses.append([int(elt) for elt in line])
        self.n = len(self.octopuses)
        self.m = len(self.octopuses[0])

    def run_multiple_steps(self, input_data, n):
        self.extract_data(input_data)
        count = 0
        for _ in range(n):
            count += self.run_one_step()
        return count

    def find_synchro(self, input_data):
        self.extract_data(input_data)
        step = 1
        size = self.n*self.m
        while self.run_one_step() != size:
            step += 1
        return step

    def run_one_step(self):
        flash_idx = []
        flash_set = set()
        count = 0
        for i in range(len(self.octopuses)):
            for j in range(len(self.octopuses[i])):
                self.octopuses[i][j] += 1
                if self.octopuses[i][j] == 10:
                    flash_idx.append((i, j))
        while len(flash_idx) > 0:
            i, j = flash_idx.pop(0)
            self.propagate_flash(i, j, flash_idx, flash_set)
            count += 1
        for i, j in flash_set:
            self.octopuses[i][j] = 0
        return count

    def propagate_flash(self, i, j, flash_idx, flash_set):
        if (i, j) in flash_set:
            return
        flash_set.add((i, j))
        for x in range(max(0, i-1), min(self.n, i+2)):
            for y in range(max(0, j-1), min(self.m, j+2)):
                if x == i and y == j:
                    continue
                if (x, y) not in flash_set:
                    self.octopuses[x][y] += 1
                    if self.octopuses[x][y] == 10:
                        flash_idx.append((x, y))

    def solution_first_star(self, input_value):
        return self.run_multiple_steps(input_value, 100)

    def solution_second_star(self, input_value):
        return self.find_synchro(input_value)
