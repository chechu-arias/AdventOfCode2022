import sys
import numpy as np


def move(actual_index, actual_x, actual_y, prev_x, prev_y):

    # check if tail is two steps away from head
    if (np.abs(prev_x - actual_x) >= 2 and prev_y == actual_y) or \
            (prev_x == actual_x and np.abs(prev_y - actual_y) >= 2) or \
            (np.abs(prev_x - actual_x) + np.abs(prev_y - actual_y) > 2):

        # identify where tail should move
        if prev_x == actual_x:
            if prev_y > actual_y:
                actual_y += 1
            elif prev_y < actual_y:
                actual_y -= 1
        elif prev_y == actual_y:
            if prev_x > actual_x:
                actual_x += 1
            elif prev_x < actual_x:
                actual_x -= 1
        else:
            if prev_x > actual_x:
                actual_x += 1
            else:
                actual_x -= 1
            if prev_y > actual_y:
                actual_y += 1
            else:
                actual_y -= 1

    if actual_index == 8:
        grid[actual_x][actual_y] = 1

    return actual_x, actual_y


with open("input_d9.txt", "r") as f:
    grid = np.zeros((5000, 5000))
    grid[2490, 0] = 1
    head_x, head_y = 2490, 0
    x = [2490, 2490, 2490, 2490, 2490, 2490, 2490, 2490, 2490]
    y = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    motions = [motion.rstrip().split(" ") for motion in f.readlines()]
    directions = {"R": 1, "L": -1, "U": -1, "D": 1}
    for motion in motions:
        for step in range(int(motion[1])):
            # head moves towards the required direction
            if motion[0] == "R" or motion[0] == "L":
                head_y += directions[motion[0]]
            elif motion[0] == "U" or motion[0] == "D":
                head_x += directions[motion[0]]
            else:
                raise Exception

            prev_x, prev_y = head_x, head_y
            for i in range(len(x)):
                actual_x, actual_y = move(i, x[i], y[i], prev_x, prev_y)
                x[i], y[i] = actual_x, actual_y
                prev_x, prev_y = x[i], y[i]

    print(f"The tail 9 visits {np.sum(grid)} positions.")
