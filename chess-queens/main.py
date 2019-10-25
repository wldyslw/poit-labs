from math import fabs
from random import shuffle

QUEEN = '♛'
BLACK = '⬛'
WHITE = '⬜'


class Queen:
    def __init__(self, coords):
        self.x, self.y = coords

    def can_beat(self, other):
        return (
            self.x == other.x or
            self.y == other.y or
            fabs(self.x - other.x) == fabs(self.y - other.y)
        )


def draw_board(queens):
    def get_empty_color(x, y):
        return BLACK if (x + y) % 2 else WHITE

    queen_coords = list(map(lambda q: (q.x, q.y), queens))
    arr = [[QUEEN if (x, y) in queen_coords else get_empty_color(x, y)
            for x in range(0, 8)] for y in range(0, 8)]

    for col in arr:
        print(' '.join(col))
    print(f'Queens are arranged, {len(queens)} total')


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
