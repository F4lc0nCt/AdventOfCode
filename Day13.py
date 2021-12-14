
from Day import Day


class Day13(Day):

    SAVE_PATH = "Day13_code.txt"

    def __init__(self):
        super().__init__(13)
        self.dict_col = None
        self.order = None
        self.max_x = None
        self.max_y = None

    def build_table(self, input_data):
        self.dict_col = {}
        self.order = []
        self.max_x = self.max_y = 0
        for line in input_data:
            if line == "":
                break
            split = line.split(',')
            x, y = int(split[0]), int(split[1])
            self.max_x = max(self.max_x, x)
            self.max_y = max(self.max_y, y)
            if x not in self.dict_col:
                self.dict_col[x] = {y}
            else:
                self.dict_col[x].add(y)
        for line in input_data:
            split = line.split(' ')[2].split('=')
            orientation, value = split[0], int(split[1])
            self.order.append((orientation, value))

    def do_folds(self, input_value, nb=None):
        self.build_table(input_value)
        idx = 0
        for orientation, value in self.order:
            if nb is not None and idx >= nb:
                break
            self.do_fold(orientation, value)
            idx += 1
        if nb is None:
            self.write_value()
        count = 0
        for k, v in self.dict_col.items():
            count += len(v)
        return count

    def do_fold(self, orientation, value):
        if orientation == 'x':
            self.do_fold_x(orientation, value)
        else:
            self.do_fold_y(orientation, value)

    def do_fold_x(self, orientation, value):
        for x in range(value + 1, self.max_x + 1):
            if x in self.dict_col:
                for y in self.dict_col[x]:
                    new_value = 2 * value - x
                    if new_value not in self.dict_col:
                        self.dict_col[new_value] = {y}
                    else:
                        self.dict_col[new_value].add(y)
                del self.dict_col[x]
        if value in self.dict_col:
            del self.dict_col[value]
        self.max_x = value - 1

    def do_fold_y(self, orientation, value):
        for y in range(value + 1, self.max_y + 1):
            for x in self.dict_col:
                if y in self.dict_col[x]:
                    self.dict_col[x].add(2 * value - y)
                    self.dict_col[x].remove(y)
        for x in self.dict_col:
            if value in self.dict_col[x]:
                self.dict_col[x].remove(value)
        self.max_y = value - 1

    def write_value(self):
        table = [[' ']*(self.max_x+1) for _ in range(self.max_y+1)]
        for x, y_set in self.dict_col.items():
            for y in y_set:
                table[y][x] = chr(9608)
        with open(self.SAVE_PATH, 'wb') as f:
            for y in range(len(table)):
                for x in range(len(table[y])):
                    f.write(table[y][x].encode('utf-8'))
                f.write('\n'.encode('utf-8'))

    def solution_first_star(self, input_value):
        return self.do_folds(input_value, nb=1)

    def solution_second_star(self, input_value):
        return self.do_folds(input_value)
