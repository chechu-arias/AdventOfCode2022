import math

import numpy as np

with open("input_d8.txt", "r") as f:
    data = f.readlines()

    height = len(data)
    width = len(data[0].replace("\n", ""))
    forest = np.zeros(shape=(width, height), dtype=np.int32)
    index = 0
    for line in data:
        line = line.rstrip()
        values = [int(x) for x in line]
        forest[index] = values
        index += 1

    visible_trees = 0
    for row in range(height):
        for col in range(width):

            if row == 0 or row == (height-1) or col == 0 or col == (width-1):
                visible_trees += 1
                continue

            current_height = forest[row, col]

            max_left = max(forest[row, :col])
            if max_left < current_height:
                visible_trees += 1
                continue

            max_right = max(forest[row, col + 1:])
            if max_right < current_height:
                visible_trees += 1
                continue

            max_above = max(forest[:row, col])
            if max_above < current_height:
                visible_trees += 1
                continue

            max_below = max(forest[row + 1:, col])
            if max_below < current_height:
                visible_trees += 1
                continue

    print(f"The number of visible trees is of {visible_trees}.")

    max_scenic_score = 0

    for row in range(height):
        for col in range(width):

            if row == 0 or row == (height - 1) or col == 0 or col == (width - 1):
                continue

            current_height = forest[row, col]

            count_left = 0
            for x in range(col):
                tree_height = forest[row, col-x-1]
                if tree_height <= current_height:
                    count_left += 1
                if current_height == tree_height:
                    break

            count_right = 0
            for x in range(col+1, width):
                tree_height = forest[row, x]
                if tree_height <= current_height:
                    count_right += 1
                if current_height == tree_height:
                    break

            count_above = 0
            for x in range(row):
                tree_height = forest[row-x-1, col]
                if tree_height <= current_height:
                    count_above += 1
                if current_height == tree_height:
                    break

            count_below = 0
            for x in range(row+1, height):
                tree_height = forest[x, col]
                if tree_height <= current_height:
                    count_below += 1
                if current_height == tree_height:
                    break

            tree_scenic_score = count_left * count_right * count_above * count_below

            if tree_scenic_score > max_scenic_score:
                max_scenic_score = tree_scenic_score

    print(f"The highest scenic score is {max_scenic_score}.")
