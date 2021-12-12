
import bisect
from Day import Day


class Day9(Day):

    def __init__(self):
        super().__init__(9)
        self.data = None
        self.low_points = None
        self.low_points_positions = None
        self.visited = None

    def extract_data(self, input_data):
        self.data = []
        for line in input_data:
            self.data.append([int(i) for i in line])

    def find_low_point(self):
        self.low_points_positions = []
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                point = self.data[i][j]
                if (i > 0 and self.data[i-1][j] <= point) or \
                   (i < len(self.data)-1 and self.data[i+1][j] <= point) or \
                   (j > 0 and self.data[i][j-1] <= point) or \
                   (j < len(self.data[i])-1 and self.data[i][j+1] <= point):
                    continue
                self.low_points_positions.append((i, j))

    def compute_risk(self, input_data):
        self.extract_data(input_data)
        self.find_low_point()
        self.low_points = [self.data[i][j] for i, j in self.low_points_positions]
        return sum(list(map(lambda x: x+1, self.low_points)))

    def delimit_basin(self, i, j):
        if (i, j) in self.visited:
            return
        self.visited.add((i, j))
        point = self.data[i][j]
        if i > 0 and self.data[i-1][j] > point and self.data[i-1][j] != 9:
            self.delimit_basin(i-1, j)
        if j > 0 and self.data[i][j-1] > point and self.data[i][j-1] != 9:
            self.delimit_basin(i, j-1)
        if i < len(self.data)-1 and self.data[i+1][j] > point and self.data[i+1][j] != 9:
            self.delimit_basin(i+1, j)
        if j < len(self.data[i])-1 and self.data[i][j+1] > point and self.data[i][j+1] != 9:
            self.delimit_basin(i, j+1)

    def find_basins(self, input_data):
        self.extract_data(input_data)
        self.find_low_point()
        ordered_basin = []
        for i, j in self.low_points_positions:
            self.visited = set()
            self.delimit_basin(i, j)
            bisect.insort(ordered_basin, len(self.visited))
        somme = 1
        for i in range(-3, 0):
            somme *= ordered_basin[i]
        return somme

    def solution_first_star(self, input_value):
        return self.compute_risk(input_value)

    def solution_second_star(self, input_value):
        return self.find_basins(input_value)

