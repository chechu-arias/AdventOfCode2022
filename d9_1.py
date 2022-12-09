import sys
import numpy as np


with open("input_d9.txt", "r") as f:
    grid = np.zeros((500, 500))
    grid[249, 0] = 1
    head_x, head_y = 249, 0
    tail_x, tail_y = 249, 0
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

            # check if tail is two steps away from head
            if (np.abs(head_x-tail_x) >= 2 and head_y == tail_y) or \
               (head_x == tail_x and np.abs(head_y-tail_y) >= 2) or \
               (np.abs(head_x-tail_x) + np.abs(head_y-tail_y) > 2):
                # identify where tail should move
                if head_x == tail_x:
                    tail_y += directions[motion[0]]
                elif head_y == tail_y:
                    tail_x += directions[motion[0]]
                else:
                    if head_x > tail_x:
                        tail_x += 1
                    else:
                        tail_x -= 1
                    if head_y > tail_y:
                        tail_y += 1
                    else:
                        tail_y -= 1

            grid[tail_x][tail_y] = 1

    print(f"The tail visits {np.sum(grid)} positions.")
