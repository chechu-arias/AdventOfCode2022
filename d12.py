import sys
import numpy as np
import string


def get_minimum(matrix):
    r, c = matrix.shape
    minimum = float('inf')
    minimum_row = -1
    minimum_column = -1
    for row in range(r):
        for column in range(c):
            if minimum > matrix[row][column] > 0:
                minimum = matrix[row][column]
                minimum_row = row
                minimum_column = column

    return minimum_row, minimum_column


def compute_part_1(initial_row, initial_column, target_row, target_column, grid):

    rows, columns = grid.shape

    visited = np.zeros((rows, columns))
    visited[initial_row][initial_column] = 1
    estimates = np.ones((rows, columns)) * float('inf')
    estimates[initial_row][initial_column] = 0

    adjacent_dict = dict()
    for row in range(rows):
        for column in range(columns):
            adjacent_dict[(row, column)] = list()
            left_column = column - 1
            if left_column >= 0:
                distance = grid[row, left_column] - grid[row, column]
                if distance <= 1:
                    adjacent_dict[(row, column)].append((row, left_column))

            right_column = column + 1
            if right_column < columns:
                distance = grid[row, right_column] - grid[row, column]
                if distance <= 1:
                    adjacent_dict[(row, column)].append((row, right_column))

            below_row = row + 1
            if below_row < rows:
                distance = grid[below_row, column] - grid[row, column]
                if distance <= 1:
                    adjacent_dict[(row, column)].append((below_row, column))

            above_row = row - 1
            if above_row >= 0:
                distance = grid[above_row, column] - grid[row, column]
                if distance <= 1:
                    adjacent_dict[(row, column)].append((above_row, column))

    current_row, current_column = initial_row, initial_column
    while visited[target_row, target_column] == 0:
        candidates = adjacent_dict[(current_row, current_column)]
        for r, c in candidates:
            if estimates[r, c] > (estimates[current_row, current_column] + 1):
                estimates[r, c] = estimates[current_row, current_column] + 1

        visited[current_row][current_column] = 1
        next_visit_matrix = (np.ones((rows, columns)) - visited) * estimates

        current_row, current_column = get_minimum(next_visit_matrix)

    return estimates[target_row, target_column]


def compute_part_2(initial_row, initial_column, all_target_points, grid):

    rows, columns = grid.shape

    visited = np.zeros((rows, columns))
    visited[initial_row][initial_column] = 1
    estimates = np.ones((rows, columns)) * float('inf')  # coste de origen hasta todos los vertices
    estimates[initial_row][initial_column] = 0

    adjacent_dict = dict()
    for row in range(rows):
        for column in range(columns):
            adjacent_dict[(row, column)] = list()
            left_column = column - 1
            if left_column >= 0:
                distance = grid[row, column] - grid[row, left_column]
                if distance <= 1:
                    adjacent_dict[(row, column)].append((row, left_column))

            right_column = column + 1
            if right_column < columns:
                distance = grid[row, column] - grid[row, right_column]
                if distance <= 1:
                    adjacent_dict[(row, column)].append((row, right_column))

            below_row = row + 1
            if below_row < rows:
                distance = grid[row, column] - grid[below_row, column]
                if distance <= 1:
                    adjacent_dict[(row, column)].append((below_row, column))

            above_row = row - 1
            if above_row >= 0:
                distance = grid[row, column] - grid[above_row, column]
                if distance <= 1:
                    adjacent_dict[(row, column)].append((above_row, column))

    current_row, current_column = initial_row, initial_column
    while True:

        if (current_row, current_column) in all_target_points:
            break

        candidates = adjacent_dict[(current_row, current_column)]
        for r, c in candidates:
            if estimates[r, c] > (estimates[current_row, current_column] + 1):
                estimates[r, c] = estimates[current_row, current_column] + 1

        visited[current_row][current_column] = 1
        next_visit_matrix = (np.ones((rows, columns)) - visited) * estimates

        current_row, current_column = get_minimum(next_visit_matrix)

    return estimates[current_row, current_column]


with open("input_d12.txt", "r") as f:

    correspondence = {letter: value for letter, value in zip(string.ascii_lowercase,
                                                             range(len(string.ascii_lowercase)))}  # elevation

    correspondence['S'] = 0
    correspondence['E'] = 25
    map_scheme = [line.rstrip() for line in f.readlines()]
    rows, columns = len(map_scheme), len(map_scheme[0])
    all_target_points = set()
    grid = np.zeros((rows, columns))
    for row in range(rows):
        for column in range(columns):
            if map_scheme[row][column] == "S":
                initial_row, initial_column = row, column
            if map_scheme[row][column] == "S" or map_scheme[row][column] == "a":
                all_target_points.add((row, column))
            if map_scheme[row][column] == "E":
                target_row, target_column = row, column
            grid[row, column] = correspondence[map_scheme[row][column]]

    res = compute_part_1(initial_row, initial_column, target_row, target_column, grid)

    print(f"The best path from start to finish needs {int(res)} steps.")

    res = compute_part_2(target_row, target_column, all_target_points, grid)

    print(f"The best path from start to finish needs {int(res)} steps.")

