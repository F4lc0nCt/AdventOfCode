import re
from Day import Day


class Board:

    def __init__(self, nb_case):
        self.nb_case = nb_case

    def compute_new_position(self, start, dice_value):
        end = (start + dice_value) % self.nb_case
        return end if end != 0 else self.nb_case


class Dice:

    def __init__(self, max_value):
        self.max_value = max_value
        self.start = 0
        self.time_roll = 0

    def roll(self):
        self.time_roll += 1
        if self.start == self.max_value:
            self.start = 1
        else:
            self.start += 1
        return self.start


class DiceMultiverse:

    def __init__(self, dim):
        self.dim = dim
        self.values = {}
        self.get_values()

    def get_values(self):
        for v in self.compute_roll(self.dim):
            self.values[v] = self.values.get(v, 0) + 1

    def compute_roll(self, n):
        if n == 1:
            return [1, 2, 3]
        res = []
        for v in self.compute_roll(n-1):
            for i in range(1, 4):
                res.append(i+v)
        return res


class Multiverses:

    TARGET_POINT = 21

    def __init__(self, multiverses_list):
        self.multiverses_list = multiverses_list
        self.p1_won = 0
        self.p2_won = 0
        self.dice = DiceMultiverse(3)
        self.board = Board(10)

    def roll(self):
        while len(self.multiverses_list) > 0:
            m = self.multiverses_list.pop()
            for v, nb_v in self.dice.values.items():
                p1 = Player(m.p1.position, m.p1.point)
                p2 = Player(m.p2.position, m.p2.point)
                new_m = Multiverse(p1, p2, Multiverse.PLAYER_1, m.nb * nb_v)
                if m.turn == Multiverse.PLAYER_1:
                    new_m.turn = Multiverse.PLAYER_2
                    new_position = self.board.compute_new_position(p1.position, v)
                    if p1.update_position(new_position, self.TARGET_POINT):
                        self.p1_won += new_m.nb
                        continue
                else:
                    new_position = self.board.compute_new_position(p2.position, v)
                    if p2.update_position(new_position, self.TARGET_POINT):
                        self.p2_won += new_m.nb
                        continue
                self.multiverses_list.append(new_m)
        return self.count_win()

    def count_win(self):
        return max(self.p1_won, self.p2_won)


class Multiverse:

    PLAYER_1 = 1
    PLAYER_2 = 2

    def __init__(self, p1, p2, turn, nb=1):
        self.p1 = p1
        self.p2 = p2
        self.turn = turn
        self.nb = nb


class Player:

    def __init__(self, position, point=0):
        self.position = position
        self.point = point

    def update_position(self, new_position, target):
        self.position = new_position
        self.point += new_position
        return self.point >= target


class Day21(Day):

    REGEX = r'Player (\d+) starting position: (\d+)'

    def __init__(self):
        super().__init__(21)
        self.board = None
        self.dice = None
        self.players = None
        self.multiverses = None

    def extract_data(self, input_value):
        self.board = Board(10)
        self.dice = Dice(100)
        self.players = {}
        for line in input_value:
            res = re.match(self.REGEX, line)
            self.players[int(res.group(1))] = Player(int(res.group(2)))

    def play_game(self, input_value):
        self.extract_data(input_value)
        stop = False
        looser = None
        while not stop:
            for i in range(1, max(self.players)+1):
                roll_value = 0
                for _ in range(3):
                    roll_value += self.dice.roll()
                new_position = self.board.compute_new_position(self.players[i].position, roll_value)
                res = self.players[i].update_position(new_position, 1000)
                if res:
                    looser = 1 if i != 1 else 2
                    stop = True
                    break
        return self.players[looser].point * self.dice.time_roll

    def extract_multiverse_data(self, input_value):
        line = next(input_value)
        res = re.match(self.REGEX, line)
        p1 = Player(int(res.group(2)))
        line = next(input_value)
        res = re.match(self.REGEX, line)
        p2 = Player(int(res.group(2)))
        multiverse = Multiverse(p1, p2, Multiverse.PLAYER_1)
        self.multiverses = Multiverses([multiverse])

    def play_multiverse_game(self, input_value):
        self.extract_multiverse_data(input_value)
        return self.multiverses.roll()

    def solution_first_star(self, input_value):
        return self.play_game(input_value)

    def solution_second_star(self, input_value):
        return self.play_multiverse_game(input_value)
