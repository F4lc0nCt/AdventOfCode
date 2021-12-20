from Day import Day


class Day20(Day):

    LIGHT_PIXEL = '#'
    DARK_PIXEL = '.'
    NB_ITERATION_FIRST_STAR = 2
    NB_ITERATION_SECOND_STAR = 50

    def __init__(self):
        super().__init__(20)
        self.algorithm = None
        self.picture = None
        self.empty_pict = None

    def extract_data(self, input_value):
        line = next(input_value)
        self.algorithm = [i == self.LIGHT_PIXEL for i in line]
        next(input_value)
        self.picture = []
        for line in input_value:
            converted_line = [i == self.LIGHT_PIXEL for i in line]
            self.picture.append(converted_line)

    def compute_empty_pict(self, n):
        self.empty_pict = [False]
        for _ in range(n):
            next_transformation = self.algorithm[-1 if self.empty_pict[-1] else 0]
            self.empty_pict.append(next_transformation)

    def print_picture(self):
        for i in range(len(self.picture)):
            string = ""
            for j in range(len(self.picture[i])):
                string += self.LIGHT_PIXEL if self.picture[i][j] else self.DARK_PIXEL
            print(string)

    def enhance_image(self, input_value, nb_times):
        self.extract_data(input_value)
        self.compute_empty_pict(nb_times)
        for i in range(nb_times):
            self.process_image(i)
        return self.count_light_pixels()

    def count_light_pixels(self):
        count = 0
        for line in self.picture:
            count += sum(map(lambda x: 1 if x else 0, line))
        return count

    def process_image(self, iteration):
        new_picture = []
        for i in range(len(self.picture) + 2):
            new_picture.append([False] * (len(self.picture[0]) + 2))
            for j in range(len(self.picture[0]) + 2):
                value = ""
                for x in range(-2, 1):
                    for y in range(-2, 1):
                        if (i + x) < 0 or (i + x) > (len(self.picture) - 1) \
                                or (j + y) < 0 or (j + y) > (len(self.picture[i + x]) - 1):
                            value += "1" if self.empty_pict[iteration] else "0"
                        else:
                            value += "1" if self.picture[i + x][j + y] else "0"
                new_picture[i][j] = self.algorithm[int(value, 2)]
        self.picture = new_picture

    def solution_first_star(self, input_value):
        return self.enhance_image(input_value, self.NB_ITERATION_FIRST_STAR)

    def solution_second_star(self, input_value):
        return self.enhance_image(input_value, self.NB_ITERATION_SECOND_STAR)
