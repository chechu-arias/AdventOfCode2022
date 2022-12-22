
import numpy as np

MATRIX_SIZE = 5000
POURING_SAND_X = 500
POURING_SAND_Y = 0


def move_sand(sand_x, sand_y, ambiente):
    if ambiente[sand_x, sand_y+1] == 0:
        return sand_x, sand_y + 1
    elif ambiente[sand_x-1, sand_y+1] == 0:
        return sand_x - 1, sand_y + 1
    elif ambiente[sand_x+1, sand_y+1] == 0:
        return sand_x + 1, sand_y + 1
    else:
        return None, None


with open("input_d14.txt", "r") as f:

    max_y = float("-inf")
    data = f.readlines()
    ambiente = np.zeros((MATRIX_SIZE, MATRIX_SIZE))
    for line in data:
        line = line.rstrip()
        rocks = line.split(" -> ")
        rocks_coords = [(int(rock.split(",")[0]), int(rock.split(",")[1])) for rock in rocks]

        max_y = max(max_y, np.max([rock[1] for rock in rocks_coords]))

        prev_coords = rocks_coords[0]
        for index in range(1, len(rocks_coords)):

            actual_coords = rocks_coords[index]

            if prev_coords[0] > actual_coords[0]:
                ambiente[actual_coords[0]:prev_coords[0]+1, actual_coords[1]] = -1
            elif prev_coords[0] < actual_coords[0]:
                ambiente[prev_coords[0]:actual_coords[0]+1, actual_coords[1]] = -1
            elif prev_coords[1] > actual_coords[1]:
                ambiente[actual_coords[0], actual_coords[1]:prev_coords[1]+1] = -1
            elif prev_coords[1] < actual_coords[1]:
                ambiente[actual_coords[0], prev_coords[1]:actual_coords[1]+1] = -1
            else:
                raise Exception

            prev_coords = actual_coords

n_sand = 0
finished = False
while True:

    sand_x, sand_y = POURING_SAND_X, POURING_SAND_Y
    while True:
        next_sand_x, next_sand_y = move_sand(sand_x, sand_y, ambiente)

        if next_sand_y is not None and next_sand_y > max_y+2:
            finished = True
            break

        if next_sand_x is None and next_sand_y is None:
            break

        sand_x, sand_y = next_sand_x, next_sand_y

    if finished:
        break

    ambiente[sand_x, sand_y] = 1
    n_sand += 1

print(f"El número de unidades de arena es de {n_sand}.")

ambiente = np.where(ambiente != -1, 0, ambiente)
ambiente[:, max_y+2] = -1

n_sand = 0
while ambiente[POURING_SAND_X, POURING_SAND_Y] != 1:

    sand_x, sand_y = POURING_SAND_X, POURING_SAND_Y
    while True:
        next_sand_x, next_sand_y = move_sand(sand_x, sand_y, ambiente)

        if next_sand_x is None and next_sand_y is None:
            break

        sand_x, sand_y = next_sand_x, next_sand_y

    ambiente[sand_x, sand_y] = 1
    n_sand += 1

print(f"El número de unidades de arena para la parte 2 es de {n_sand}.")
