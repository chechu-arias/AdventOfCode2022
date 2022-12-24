
import sys
import numpy as np
np.set_printoptions(threshold=sys.maxsize)


CHAMBER_HEIGHT = 3
CHAMBER_WIDTH = 7
FIGURES = [
    [[0, 0, 0, 0]],
    [[-1, 0, -1],
     [0, 0, 0],
     [-1, 0, -1]],
    [[-1, -1, 0],
     [-1, -1, 0],
     [0, 0, 0]],
    [[0],
     [0],
     [0],
     [0]],
    [[0, 0],
     [0, 0]]
]

FIGURES_SHIFT_LEFT_TOP = [
    0, 1, 2, 0, 0
]

with open("input_d17.txt", "r") as f:
    air_pattern = f.readlines()[0].rstrip()


def redraw_current_scenary(current_scenary, next_figure):

    for index, row in enumerate(current_scenary):
        if 1 in row:
            break

    rows_left = current_scenary.shape[0] - index
    new_scenary = np.zeros(((len(next_figure) + CHAMBER_HEIGHT + rows_left), CHAMBER_WIDTH))
    new_scenary[new_scenary.shape[0] - rows_left:, :] = current_scenary[current_scenary.shape[0] - rows_left:]

    return new_scenary


def draw_figure(current_scenary, figure, left_x, up_y, value):
    for n_col in range(len(figure)):
        col = figure[n_col]
        for n_row in range(len(col)):
            figure_pixel = figure[n_col][n_row]
            if figure_pixel == 0:
                current_scenary[left_x + n_col, up_y + n_row] = value


def check_all_zeros_figure(current_scenary, figure, left_x, up_y):
    for n_col in range(len(figure)):
        col = figure[n_col]
        for n_row in range(len(col)):
            figure_pixel = figure[n_col][n_row]
            if figure_pixel == 0:
                if (left_x + n_col) >= current_scenary.shape[0] or current_scenary[left_x + n_col, up_y + n_row] != 0:
                    return False
    return True


def drawing_out_of_map_figure(current_scenary, figure, left_x, up_y):
    for n_col in range(len(figure)):
        col = figure[n_col]
        for n_row in range(len(col)):
            figure_pixel = figure[n_col][n_row]
            if figure_pixel == 0:
                if (left_x + n_col) >= current_scenary.shape[0]:
                    return True
    return False


def visualization(current_scenary, max_rows):
    s = ''

    n_printed = 0
    for n_row in range(len(current_scenary)):
        row = current_scenary[n_row]
        for n_col in range(len(row)):
            if current_scenary[n_row, n_col] == -1:
                s += '@'
            elif current_scenary[n_row, n_col] == 1:
                s += '#'
            else:
                s += '.'
        s += '\n'
        n_printed += 1
        if max_rows is not None and n_printed > max_rows:
            break

    return s


def move_figure(current_scenary, figure, figure_index, air_pattern):

    moved = True

    upper_row, upper_col = -1, -1
    for i in range(current_scenary.shape[0]):
        if -1 in current_scenary[i]:
            upper_row = i
            upper_col = np.where(current_scenary[i] == -1)[0][0]
            upper_col -= FIGURES_SHIFT_LEFT_TOP[figure_index]
            break

    # No figure painted
    if upper_col == -1 and upper_row == -1:

        upper_row = 0
        upper_col = 2
        draw_figure(current_scenary, figure, upper_row, upper_col, -1)

        upper_row, upper_col = -1, -1
        for i in range(current_scenary.shape[0]):
            if -1 in current_scenary[i]:
                upper_row = i
                upper_col = np.where(current_scenary[i] == -1)[0][0]
                upper_col -= FIGURES_SHIFT_LEFT_TOP[figure_index]
                break

    # Clear figure and have positions
    current_scenary[current_scenary == -1] = 0

    under_row = upper_row + 1

    air_col = upper_col
    if air_pattern == ">" and (upper_col + len(figure[0])) < 7:
        air_col += 1
    elif air_pattern == "<" and (upper_col - 1) >= 0:
        air_col -= 1

    # Abajo lado
    if (check_all_zeros_figure(current_scenary, figure, upper_row, air_col) and
            check_all_zeros_figure(current_scenary, figure, under_row, air_col)):
        draw_figure(current_scenary, figure, under_row, air_col, -1)

    # Fin Lado
    elif check_all_zeros_figure(current_scenary, figure, upper_row, air_col):
        draw_figure(current_scenary, figure, upper_row, air_col, 1)
        moved = False

    # Abajo
    elif check_all_zeros_figure(current_scenary, figure, under_row, upper_col):
        draw_figure(current_scenary, figure, under_row, upper_col, -1)

    # Fin abajo
    elif check_all_zeros_figure(current_scenary, figure, under_row, upper_col):
        draw_figure(current_scenary, figure, under_row, upper_col, 1)
        moved = False

    # Fin sitio
    else:
        draw_figure(current_scenary, figure, upper_row, upper_col, 1)
        moved = False

    return moved


n_figures = 0
figure_index = 0
pattern_index = 0
current_scenary = np.zeros(((len(FIGURES[figure_index])+CHAMBER_HEIGHT), CHAMBER_WIDTH))

while n_figures < 1_000_000_000_000:

    if n_figures > 0 and n_figures % 100_000_000 == 0:
        print(f"{n_figures} out of 1000000000000")

    figure = FIGURES[figure_index % len(FIGURES)]
    air_now = air_pattern[pattern_index % len(air_pattern)]

    moved = move_figure(current_scenary, figure, (figure_index % len(FIGURES)), air_now)

    if not moved:
        n_figures += 1
        figure_index += 1
        current_scenary = redraw_current_scenary(current_scenary, FIGURES[figure_index % len(FIGURES)])

    pattern_index += 1


for index, row in enumerate(current_scenary):
    if 1 in row:
        break

rows_left = current_scenary.shape[0] - index

print(f"The tower of rocks will be of {rows_left} units.")
