from math import fabs
from random import shuffle

QUEEN = '♛'
# EMPTY = '▢'
EMPTY = '0'


class Queen:
    def __init__(self, coords):
        self.x, self.y = coords

    def can_beat(self, other):
        return (
            self.x == other.x or
            self.y == other.y or
            fabs(self.x - other.x) == fabs(self.y - other.y)
        )

    def __repr__(self):
        return f'<Queen(x={self.x}, y={self.y})>'


def draw_board(queens):
    queen_coords = list(map(lambda q: (q.x, q.y), queens))
    arr = [[QUEEN if (x, y) in queen_coords else EMPTY for x in range(0, 8)] for y in range(0, 8)]

    for col in arr:
        print(' '.join(col))


def main():
    queens = []
    turns = [(x, y) for x in range(0, 8) for y in range(0, 8)]
    shuffle(turns)

    for turn in turns:
        queen = Queen(turn)
        if not any(map(lambda q: q.can_beat(queen), queens)):
            queens.append(queen)

    draw_board(queens)


main()
