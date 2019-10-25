from random import shuffle, randrange
from math import fabs

shifts = [-2, -1, 1, 2]
available_moves = [(i, j)
                   for i in shifts for j in shifts if fabs(i) != fabs(j)]


def go(board, x, y):
    try_order = [i for i in range(8)]
    shuffle(try_order)
    for i in try_order:
        new_x = x + available_moves[i][0]
        new_y = y + available_moves[i][1]
        if 0 <= new_x < 8 and 0 <= new_y < 8 and board[new_x][new_y] == 0:
            return (new_x, new_y)

    return (x, y)


def print_moves(board):
    lines = ['───' for _ in range(8)]
    board_top_join    = f"┌{'┬'.join(lines)}┐\n"
    board_middle_join = f"├{'┼'.join(lines)}┤\n"
    board_bottom_join = f"└{'┴'.join(lines)}┘\n"
    rows = []
    for row in board:
        rows.append(
            f"|{'|'.join(f'{x or str():^3}' for x in row)}|\n")
    print(f'{board_top_join}{board_middle_join.join(rows)}{board_bottom_join}')


def main():
    board = [[0 for i in range(8)] for j in range(8)]
    x = randrange(8)
    y = randrange(8)
    move_count = 0
    while True:
        (new_x, new_y) = go(board, x, y)
        if new_x != x and new_y != y:
            move_count += 1
            board[new_x][new_y] = move_count
            x, y = new_x, new_y
        else:
            break
    print_moves(board)
    print(f'Finished with total of {move_count} moves')


main()
