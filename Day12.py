
from Day import Day


class Day12(Day):

    START = 'start'
    END = 'end'

    def __init__(self):
        super().__init__(12)
        self.dict_edge = None

    def build_graph(self, input_data):
        self.dict_edge = {}
        for line in input_data:
            split = line.split('-')
            s, e = split[0], split[1]
            self.dict_edge[s] = self.dict_edge.get(s, []) + [e]
            self.dict_edge[e] = self.dict_edge.get(e, []) + [s]

    def find_path_from(self, src, dst, visited):
        if src == dst:
            return [[dst]]
        if str.islower(src):
            if src in visited:
                return []
            else:
                visited.add(src)
        paths = []
        for e in self.dict_edge[src]:
            sub_paths = self.find_path_from(e, dst, visited.copy())
            paths += [[src] + p for p in sub_paths]
        return paths

    def find_path_multi_from(self, src, dst, visited, twice):
        if src == dst:
            return [[dst]]
        next_twice = twice
        if str.islower(src):
            if src in visited:
                if twice or src == self.START:
                    return []
                next_twice = True
            else:
                visited.add(src)
        paths = []
        for e in self.dict_edge[src]:
            sub_paths = self.find_path_multi_from(e, dst, visited.copy(), next_twice)
            paths += [[src] + p for p in sub_paths]
        return paths

    def find_path(self, input_data):
        self.build_graph(input_data)
        paths = self.find_path_from(self.START, self.END, set())
        return len(paths)

    def find_path_multi(self, input_data):
        self.build_graph(input_data)
        paths = self.find_path_multi_from(self.START, self.END, set(), False)
        return len(paths)

    def solution_first_star(self, input_value):
        return self.find_path(input_value)

    def solution_second_star(self, input_value):
        return self.find_path_multi(input_value)
