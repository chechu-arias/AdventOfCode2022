
import string

total_priorities = 0
LETTER_TO_PRIORITY = {string.ascii_letters[i]: i+1 for i in range(len(string.ascii_letters))}
with open("input_d3.txt", "r") as f:
    for line in f:
        line = line.replace("\n", "")
        len_m = len(line) // 2
        left, right = set(line[:len_m]), set(line[len_m:])
        total_priorities += LETTER_TO_PRIORITY[list(left.intersection(right))[0]]

print(f"The sum of priorities for part 1 is {total_priorities}.")

total_priorities = 0
with open("input_d3.txt", "r") as f:
    index = 0
    rucksack = list()
    for line in f:
        line = line.replace("\n", "")
        if index > 0 and index % 3 == 2:
            rucksack.append(set(line))
            intersec = rucksack[0].intersection(rucksack[1])
            intersec = intersec.intersection(rucksack[2])
            total_priorities += LETTER_TO_PRIORITY[list(intersec)[0]]
            rucksack = list()
        else:
            rucksack.append(set(line))
        index += 1

print(f"The sum of priorities for part 2 is {total_priorities}.")
