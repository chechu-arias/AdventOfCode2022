
with open("input_d18.txt", "r") as f:
    data = f.readlines()

min_x = float("inf")
min_y = float("inf")
min_z = float("inf")
max_x = -1
max_y = -1
max_z = -1

cubes = dict()
for line in data:
    line = line.rstrip().split(",")
    line = list(map(int, line))
    x, y, z = line[0], line[1], line[2]

    min_x = min(min_x, x)
    min_y = min(min_y, y)
    min_z = min(min_z, z)

    max_x = max(max_x, x)
    max_y = max(max_y, y)
    max_z = max(max_z, z)

    n_adjacent = 0
    adjacents = [
        (x - 1, y, z),
        (x + 1, y, z),
        (x, y - 1, z),
        (x, y + 1, z),
        (x, y, z - 1),
        (x, y, z + 1)
    ]
    for adj_coords in adjacents:
        if adj_coords in cubes:
            cubes[adj_coords] -= 1
            n_adjacent += 1

    cubes[(x, y, z)] = 6 - n_adjacent

print(f"The total number of sides not connected is {sum(cubes.values())}.")

