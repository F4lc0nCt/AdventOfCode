
from enum import Enum
from Day import Day


class Day4(Day):

    def __init__(self):
        super().__init__(4)
        self.drawn_data = []
        self.boards = []
        self.dict_board = {}
        self.nb_not_none = 0

    def build_data(self, text_input):
        self.drawn_data = []
        self.boards = []
        self.dict_board = {}
        drawn_string = next(text_input)
        for v in drawn_string.split(','):
            self.drawn_data.append(int(v))
        idx_board = 0
        while next(text_input, None) is not None:
            bd = []
            x = 0
            for _ in range(5):
                line_board = []
                line = next(text_input)
                y = 0
                for v in line.split(' '):
                    if v != '':
                        line_board.append((int(v),False))
                        if int(v) in self.dict_board:
                            self.dict_board[int(v)].append((idx_board, x, y))
                        else:
                            self.dict_board[int(v)] = [(idx_board, x, y)]
                        y += 1
                x += 1
                bd.append(line_board)
            self.boards.append(bd)
            idx_board += 1
        self.nb_not_none = idx_board

    def check_all_boards(self):
        for board in self.boards:
            res = self.check_board(board)
            if res:
                return self.compute_points(board)
        return None

    def compute_bingo(self, bingo_values):
        self.build_data(bingo_values)
        for i in self.drawn_data:
            if i in self.dict_board:
                for board, x, y in self.dict_board[i]:
                    self.boards[board][x][y] = (i, True)
            possible_points = self.check_all_boards()
            if possible_points is not None:
                return i*possible_points

    def check_all_boards_2(self):
        idx = 0
        while idx < len(self.boards):
            res = self.check_board(self.boards[idx])
            if res and self.nb_not_none > 1:
                self.nb_not_none -= 1
                self.boards[idx] = None
            elif res and self.nb_not_none == 1:
                return idx
            else:
                idx += 1
        return None

    def compute_bingo_2(self, bingo_values):
        self.build_data(bingo_values)
        for i in self.drawn_data:
            if i in self.dict_board:
                for board, x, y in self.dict_board[i]:
                    if self.boards[board] is not None:
                        self.boards[board][x][y] = (i, True)
            possible_idx = self.check_all_boards_2()
            if possible_idx is not None:
                possible_points = self.compute_points(self.boards[possible_idx])
                return possible_points*i

    def solution_first_star(self, input_value):
        return self.compute_bingo(input_value)

    def solution_second_star(self, input_value):
        return self.compute_bingo_2(input_value)

    @staticmethod
    def compute_points(board):
        points = 0
        for x in range(5):
            for y in range(5):
                val, state = board[x][y]
                if not state:
                    points += val
        return points

    @staticmethod
    def check_board(board):
        if board is None:
            return False
        for x in range(5):
            flag_row = True
            flag_col = True
            for y in range(5):
                _, flag = board[x][y]
                flag_row &= flag
                _, flag = board[y][x]
                flag_col &= flag
                if not flag_row and not flag_col:
                    break
            else:
                return True
        return False
