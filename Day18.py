from Day import Day


class SnailFish:

    SPLIT_THRESHOLD = 9

    def __init__(self, left, right, level):
        self.left = left
        self.right = right
        self.level = level

    @staticmethod
    def build_snail(line, level):
        if line[0] != '[':
            return int(line[0])
        count = 0
        stop = None
        for i in range(1, len(line) - 1):
            if line[i] == '[':
                count += 1
            elif line[i] == ']':
                count -= 1
            elif line[i] == ',' and count == 0:
                stop = i
                break
        left = SnailFish.build_snail(line[1:stop], level+1)
        right = SnailFish.build_snail(line[stop+1:-1], level+1)
        return SnailFish(left, right, level)

    def update_level(self, new_level):
        self.level = new_level
        if isinstance(self.left, SnailFish):
            self.left.update_level(new_level+1)
        if isinstance(self.right, SnailFish):
            self.right.update_level(new_level+1)

    @staticmethod
    def add_snail(left_snail, right_snail):
        res = SnailFish(left_snail.copy(), right_snail.copy(), left_snail.level)
        res.update_level(left_snail.level)
        res.reduce_snail()
        return res

    def reduce_snail(self):
        res = True
        while res:
            res, _, _ = self.reduced_nested()
        while self.reduced_split():
            res = True
            while res:
                res, _, _ = self.reduced_nested()

    def reduced_nested(self):
        if self.level == 4:
            return self.reduce_max_level()
        else:
            return self.propagate_reduce()

    def reduce_max_level(self):
        if isinstance(self.left, SnailFish):
            lt = self.left.left
            if isinstance(self.right, SnailFish):
                self.right.left += self.left.right
                self.left = 0
            else:
                self.right += self.left.right
                self.left = 0
            return True, lt, None
        elif isinstance(self.right, SnailFish):
            rt = self.right.right
            self.left += self.right.left
            self.right = 0
            return True, None, rt
        return False, None, None

    def propagate_reduce(self):
        if isinstance(self.left, SnailFish):
            result, left_rt, right_rt = self.propagate_reduce_left()
            if result:
                return result, left_rt, right_rt
        if isinstance(self.right, SnailFish):
            result, left_rt, right_rt = self.propagate_reduce_right()
            if result:
                return result, left_rt, right_rt
        return False, None, None

    def propagate_reduce_left(self):
        result, left_rt, right_rt = self.left.reduced_nested()
        if right_rt is not None:
            if isinstance(self.right, SnailFish):
                self.right.add_to_left(right_rt)
            else:
                self.right += right_rt
        if result:
            return True, left_rt, None
        return False, None, None

    def propagate_reduce_right(self):
        result, left_rt, right_rt = self.right.reduced_nested()
        if left_rt is not None:
            if isinstance(self.left, SnailFish):
                self.left.add_to_right(left_rt)
            else:
                self.left += left_rt
        if result:
            return True, None, right_rt
        return False, None, None

    def add_to_left(self, value):
        if isinstance(self.left, SnailFish):
            self.left.add_to_left(value)
        else:
            self.left += value

    def add_to_right(self, value):
        if isinstance(self.right, SnailFish):
            self.right.add_to_right(value)
        else:
            self.right += value

    def reduced_split(self):
        if isinstance(self.left, SnailFish):
            if self.left.reduced_split():
                return True
        elif self.left > self.SPLIT_THRESHOLD:
            new_left = new_right = self.left//2
            new_right += self.left % 2
            self.left = SnailFish(new_left, new_right, self.level+1)
            return True
        if isinstance(self.right, SnailFish):
            if self.right.reduced_split():
                return True
        elif self.right > self.SPLIT_THRESHOLD:
            new_left = new_right = self.right // 2
            new_right += self.right % 2
            self.right = SnailFish(new_left, new_right, self.level + 1)
            return True
        return False

    def compute_magnitude(self):
        magnitude = 0
        if isinstance(self.left, SnailFish):
            magnitude += 3*self.left.compute_magnitude()
        else:
            magnitude += 3*self.left
        if isinstance(self.right, SnailFish):
            magnitude += 2*self.right.compute_magnitude()
        else:
            magnitude += 2*self.right
        return magnitude

    def __str__(self):
        return f'[{self.left}, {self.right}]'

    def copy(self):
        obj = SnailFish(None, None, self.level)
        if isinstance(self.left, SnailFish):
            obj.left = self.left.copy()
        else:
            obj.left = self.left
        if isinstance(self.right, SnailFish):
            obj.right = self.right.copy()
        else:
            obj.right = self.right
        return obj


class Day18(Day):

    def __init__(self):
        super().__init__(18)
        self.snail_list = None

    def extract_data(self, input_value):
        self.snail_list = []
        for line in input_value:
            if line == "":
                break
            self.snail_list.append(SnailFish.build_snail(line, 1))

    def do_addition(self, input_value):
        self.extract_data(input_value)
        curr_snail = self.snail_list.pop(0)
        while len(self.snail_list) > 0:
            curr_snail = SnailFish.add_snail(curr_snail, self.snail_list.pop(0))
        return curr_snail.compute_magnitude()

    def max_sum_of_two(self, input_value):
        self.extract_data(input_value)
        max_magnitude = 0
        for i in range(len(self.snail_list)-1):
            for j in range(i+1, len(self.snail_list)):
                res = SnailFish.add_snail(self.snail_list[i], self.snail_list[j]).compute_magnitude()
                max_magnitude = max(max_magnitude, res)
                res = SnailFish.add_snail(self.snail_list[j], self.snail_list[i]).compute_magnitude()
                max_magnitude = max(max_magnitude, res)
        return max_magnitude

    def solution_first_star(self, input_value):
        return self.do_addition(input_value)

    def solution_second_star(self, input_value):
        return self.max_sum_of_two(input_value)
