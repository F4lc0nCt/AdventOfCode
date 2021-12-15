import sys
import networkx as nx


from Day import Day


class Day15(Day):

    WEIGHT = 'weight'
    NB_EXTENSION = 5
    MAX_RISK = 9

    def __init__(self):
        super().__init__(15)
        self.risk_map = None
        self.i_max = None
        self.j_max = None

    def extract_risk_map(self, input_data):
        self.risk_map = nx.DiGraph()
        i = 0
        prev_data = []
        for line in input_data:
            data = [int(v) for v in line]
            for j in range(len(data)):
                if i > 0:
                    self.risk_map.add_edge((i - 1, j), (i, j))
                    self.risk_map[(i - 1, j)][(i, j)][self.WEIGHT] = data[j]
                    self.risk_map.add_edge((i, j), (i - 1, j))
                    self.risk_map[(i, j)][(i - 1, j)][self.WEIGHT] = prev_data[j]
                if j > 0:
                    self.risk_map.add_edge((i, j-1), (i, j))
                    self.risk_map[(i, j-1)][(i, j)][self.WEIGHT] = data[j]
                    self.risk_map.add_edge((i, j), (i, j - 1))
                    self.risk_map[(i, j)][(i, j - 1)][self.WEIGHT] = data[j-1]
            i += 1
            prev_data = data.copy()
        self.i_max = i-1
        self.j_max = j

    def find_low_risk(self, input_data, extend=False):
        if extend:
            self.extract_extended_data(input_data)
        else:
            self.extract_risk_map(input_data)
        return nx.shortest_path_length(self.risk_map, (0, 0), (self.i_max, self.j_max), self.WEIGHT)

    def find_low_risk_from(self, i, j, visited):
        if (i, j) in visited:
            return visited[(i, j)]
        right = down = sys.maxsize
        if j < self.j_max:
            right = self.find_low_risk_from(i, j+1, visited)
        if i < self.i_max:
            down = self.find_low_risk_from(i+1, j, visited)
        visited[(i, j)] = self.risk_map[i][j] + min(right, down)
        return visited[(i, j)]

    def process_value(self, line, e, i):
        val = int(e) + i
        line.append(val % self.MAX_RISK if val > self.MAX_RISK else val)

    def extract_extended_data(self, input_data):
        base_data = []
        for line in input_data:
            new_line = []
            for i in range(5):
                for e in line:
                    self.process_value(new_line, e, i)
            base_data.append(new_line)
        length_base = len(base_data)
        for i in range(1, 5):
            for idx in range(length_base):
                new_line = []
                for e in base_data[idx]:
                    self.process_value(new_line, e, i)
                base_data.append(new_line)
        self.extract_risk_map(base_data)

    def solution_first_star(self, input_value):
        return self.find_low_risk(input_value)

    def solution_second_star(self, input_value):
        return self.find_low_risk(input_value, True)
