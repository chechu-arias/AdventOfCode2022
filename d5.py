
import copy

with open("input_d5.txt", "r") as f:

    data = f.readlines()

    stack_length = -1
    reading_stack = True
    stack = [list() for i in range(100)]
    movements = list()

    for line in data:

        line = line.replace("\n", "")

        # Reading stacks information
        if reading_stack and any(c.isalpha() for c in line):
            for i in range((len(line)//4)+1):
                elem = line[i*4:(i+1)*4]
                if elem[1] != " ":
                    stack[i].append(elem[1])
                    if i > stack_length:
                        stack_length = i
        else:
            reading_stack = False

        # Reading movements made
        if not reading_stack and len(line) > 0 and line[0].isalpha():
            words = line.split()
            n_moves, stack_orig, stack_dest = int(words[1]), int(words[3]), int(words[5])
            movements.append((n_moves, stack_orig, stack_dest))

    # Making the movements
    stack = stack[:stack_length+1]
    stack_part_2 = copy.deepcopy(stack)
    for m in movements:

        n_moves, stack_orig, stack_dest = m

        moved_list = list()
        moved_list_part_2 = list()
        for i in range(n_moves):
            moved_list.append(stack[stack_orig-1].pop(0))
            moved_list_part_2.append(stack_part_2[stack_orig-1].pop(0))

        moved_list.reverse()
        stack[stack_dest-1] = moved_list + stack[stack_dest-1]

        stack_part_2[stack_dest - 1] = moved_list_part_2 + stack_part_2[stack_dest - 1]

res = ""
for i in range(stack_length+1):
    res += stack[i][0]

print(f"The result at the end of the top of the stacks for part 1 is {res}.")

res = ""
for i in range(stack_length+1):
    res += stack_part_2[i][0]

print(f"The result at the end of the top of the stacks for part 2 is {res}.")
