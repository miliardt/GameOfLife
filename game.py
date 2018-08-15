import unittest
import copy
import math


class Board():

    def __init__(self, board):
        self.board = board

    def __len__(self):
        return len(self.board)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, Board):
            return False
        return self.board.__eq__(o.board)

    def __iter__(self):
        return self.board.__iter__()

    def __getitem__(self, key):
        if type(key) == int:
            return self.board[key]
        i, j = key
        if i < 0 or i >= len(self.board):
            return None
        if j < 0 or j >= len(self.board[i]):
            return None
        return self.board[i][j]

    def __setitem__(self, key, value):
        i, j = key
        self.board[i][j] = value

    def __str__(self) -> str:
        return self.board.__str__()

    def __repr__(self) -> str:
        return self.__str__()

    def counting_chars(self, char):
        char_counter = 0
        for row in self.board:
            for cell in row:
                if cell == char:
                    char_counter += 1
        return char_counter

    def print_board(self):
        s = ''
        for row in self.board:
            print(s.join(row))

    @staticmethod
    def create(m, n, char=' '):
        board = []
        for item in range(m):
            row = [char] * n
            board.append(row)
        return Board(board)

    @staticmethod
    def read(string_board):
        board = []
        table_row = string_board.split('\n')
        for line in table_row:
            row = list(line)
            board.append(row)
        return Board(board)

    def list_neighbours(self, i, j):
        neighbours = []
        if self[i - 1, j - 1]: neighbours.append(self[i - 1, j - 1])
        if self[i - 1, j]: neighbours.append(self[i - 1, j])
        if self[i - 1, j + 1]: neighbours.append(self[i - 1, j + 1])
        if self[i, j + 1]: neighbours.append(self[i, j + 1])
        if self[i + 1, j + 1]: neighbours.append(self[i + 1, j + 1])
        if self[i + 1, j]: neighbours.append(self[i + 1, j])
        if self[i + 1, j - 1]: neighbours.append(self[i + 1, j - 1])
        if self[i, j - 1]: neighbours.append(self[i, j - 1])
        return neighbours


class GameOfLife():
    ALIVE = '*'
    DEAD = ' '

    def __init__(self):
        self.i_max = None
        self.i_min = None
        self.j_min = None
        self.j_max = None

    def step(self, board):
        self.reset_min_max()
        new_board = copy.deepcopy(board)
        for i in range(len(board)):
            for j in range(len(board[i])):
                cell = board[i][j]
                live_neighbours = self.live_neighbours_count(i, j, board)
                if live_neighbours < 2 and cell == self.ALIVE:
                    new_board[i][j] = self.DEAD
                elif live_neighbours > 3 and cell == self.ALIVE:
                    new_board[i][j] = self.DEAD
                elif live_neighbours == 3 and cell == self.DEAD:
                    new_board[i][j] = self.ALIVE
                elif (live_neighbours == 3 or live_neighbours == 2) and cell == self.ALIVE:
                    new_board[i][j] = self.ALIVE
        return new_board

    def reset_min_max(self):
        self.i_max = 0
        self.i_min = math.inf
        self.j_min = math.inf
        self.j_max = 0

    def set_alive(self, board, i, j):
        board[i, j] = self.ALIVE
        if i < self.i_min: self.i_min= i
        if i > self.i_max: self.i_max= i
        if j < self.j_min: self.j_min= j
        if j > self.j_max: self.j_max= j

    def live_neighbours_count(self, i, j, board):
        return board.list_neighbours(i, j).count(self.ALIVE)


def from_lines(*args):
    return '\n'.join(args)


class TestBoard(unittest.TestCase):

    def test_char_in_board(self):
        board = Board.create(4, 5, "*")
        self.assertEqual(4 * 5, board.counting_chars("*"))
        self.assertEqual(0, board.counting_chars(" "))

        board[3, 3] = '4'
        self.assertEqual(1, board.counting_chars('4'))

    def test_board(self):
        board = Board.create(5, 6, ' ')
        self.assertEqual(5, len(board))

        for row in board:
            self.assertEqual(6, len(row))
            for cell in row:
                self.assertEqual(' ', cell)

    def test_read_board(self):
        board_string = from_lines(
            "* *",
            "** "
        )
        board = Board.read(board_string)
        self.assertEqual(['*', ' ', '*'], list(board[0]))
        self.assertEqual(['*', '*', ' '], list(board[1]))

    def test_out_of_range(self):
        board = Board.create(5, 5, '*')
        self.assertEqual('*', board[3, 3])
        self.assertEqual(None, board[6, 3])
        self.assertEqual(None, board[3, 6])


class TestGameOfLife(unittest.TestCase):
    still_boards = [Board.read(from_lines('    ',
                                          ' ** ',
                                          ' ** ',
                                          '    ')),
                    Board.read(from_lines('      ',
                                          '  **  ',
                                          ' *  * ',
                                          '  **  ',
                                          '      '))]

    def test_still_boards(self):
        for board in self.still_boards:
            game = GameOfLife()
            self.assertEqual(board, game.step(board))

    def test_oscillate_boards(self):
        game = GameOfLife()

        self.assertEqual(Board.read(from_lines('     ',
                                               '  *  ',
                                               '  *  ',
                                               '  *  ',
                                               '     ')),
                         game.step(Board.read(from_lines('     ',
                                                         '     ',
                                                         ' *** ',
                                                         '     ',
                                                         '     ')))
                         )


if __name__ == '__main__':
    unittest.main()

board = Board.create(6, 7, '*')
board[2, 3] = '#'
board.print_board()
