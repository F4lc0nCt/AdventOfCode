from Day import Day


class ComputationError(Exception):

    def __init__(self, pointer, message):
        self.pointer = pointer
        self.message = message
        super().__init__(self.message)


class Day24(Day):

    def __init__(self):
        super().__init__(24)
        self.instruction = None
        self.mem = {'w': 0, 'x': 0, 'y': 0, 'z': 0}

    def extract_data(self, input_value):
        self.instruction = []
        for line in input_value:
            if len(line) == 0:
                break
            self.instruction.append(line.split(' '))

    def compute(self, model):
        self.mem = {'w': 0, 'x': 0, 'y': 0, 'z': 0}
        pointer = 0
        for ins in self.instruction:
            if ins[0] == 'inp':
                self.mem[ins[1]] = int(model[pointer])
                pointer += 1
                continue
            val = self.mem[ins[2]] if ins[2] in self.mem else int(ins[2])
            if ins[0] == 'add':
                self.mem[ins[1]] += val
            elif ins[0] == 'mul':
                self.mem[ins[1]] *= val
            elif ins[0] == 'div':
                if val == 0:
                    raise ComputationError(pointer, 'Error at div '+str(pointer))
                self.mem[ins[1]] //= val
            elif ins[0] == 'mod':
                if self.mem[ins[1]] < 0 or val <= 0:
                    raise ComputationError(pointer, 'Error at mod '+str(pointer))
                self.mem[ins[1]] %= val
            elif ins[0] == 'eql':
                self.mem[ins[1]] = 1 if self.mem[ins[1]] == val else 0
        return self.mem['z'] == 0

    def generate_monad_max(self, input_value):
        """
        Constrain computed bu hand
        w[5] = w[2]-2
        w[3] = w[4]
        w[8] = w[7]+4
        w[9] = w[6]-8
        w[11] = w[10]-5
        w[12] = w[1]-4
        w[13] = w[0]-4
        """
        self.extract_data(input_value)
        model_max = 99999795919456
        return model_max if self.compute(str(model_max)) else None

    def generate_monad_min(self, input_value):
        """
        Constrain computed bu hand
        w[5] = w[2]-2
        w[3] = w[4]
        w[8] = w[7]+4
        w[9] = w[6]-8
        w[11] = w[10]-5
        w[12] = w[1]-4
        w[13] = w[0]-4
        """
        self.extract_data(input_value)
        model_min = 45311191516111
        return model_min if self.compute(str(model_min)) else None

    def solution_first_star(self, input_value):
        return self.generate_monad_max(input_value)

    def solution_second_star(self, input_value):
        return self.generate_monad_min(input_value)
