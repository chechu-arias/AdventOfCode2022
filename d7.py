import math

DISK_SPACE = 70000000
UPDATE_SPACE = 30000000


def add_all_values_of_dict(dct):
    total = [0]
    for key, value in dct.items():
        if isinstance(value, int):
            total[0] += value
        if isinstance(value, str):
            total.append(value)
        if isinstance(value, dict):
            aux = add_all_values_of_dict(value)
            total[0] += aux.pop(0)
            total.extend(aux)
    return total


with open("input_d7.txt", "r") as f:

    data = f.readlines()

    index = 0
    structure = dict()
    current_dir = ""
    while index < len(data):
        line = data[index].rstrip()
        elements = line.split()
        if line.startswith("$"):

            if elements[1] == "ls":

                next_line = data[index+1].rstrip()
                while not next_line.startswith("$"):
                    next_line_elements = next_line.split()
                    if next_line_elements[0] == "dir":
                        structure[current_dir + next_line_elements[1] + "/"] = {}
                        structure[current_dir][next_line_elements[1] + "/"] = current_dir + next_line_elements[1] + "/"
                    else:
                        if current_dir not in structure:
                            structure[current_dir] = {}
                        if next_line_elements[1] not in structure[current_dir]:
                            structure[current_dir][next_line_elements[1]] = int(next_line_elements[0])
                    index += 1
                    if (index+1) == len(data):
                        break
                    next_line = data[index+1].rstrip()

            elif elements[1] == "cd":

                if elements[2] == "..":
                    current_dir = current_dir[:-1]
                    while current_dir[-1].isalnum():
                        current_dir = current_dir[:-1]
                else:
                    current_dir += elements[2].replace("/", "") + "/"
                    if current_dir not in structure:
                        structure[current_dir] = {}

        index += 1

    all_numbers = True
    structure_numbers = dict()
    for current_dir, dirs_d in structure.items():
        res = add_all_values_of_dict(dirs_d)
        if any([isinstance(x, str) for x in res]):
            all_numbers = False
        structure_numbers[current_dir] = res

    while not all_numbers:
        all_numbers = True
        for current_dir, dirs_d in structure_numbers.items():
            aux = list()
            for elem in dirs_d:
                if isinstance(elem, str):
                    aux.extend(structure_numbers[elem])
                else:
                    aux.append(elem)
            structure_numbers[current_dir] = aux
            if any([isinstance(x, str) for x in aux]):
                all_numbers = False

    total_sum = 0
    for current_dir, dir_list_size in structure_numbers.items():
        if sum(dir_list_size) < 100000:
            total_sum += sum(dir_list_size)
        structure_numbers[current_dir] = sum(dir_list_size)

    print(f"The total sum of specified directories is of {total_sum}.")

    used_space = structure_numbers["/"]
    empty_space = DISK_SPACE - used_space
    needed_space = UPDATE_SPACE - empty_space

    closest_value = math.inf
    for current_dir, dir_size in structure_numbers.items():
        if needed_space <= dir_size < closest_value and closest_value > 0:
            closest_value = dir_size

    print(f"The directory you have to delete has a size of {closest_value}.")

