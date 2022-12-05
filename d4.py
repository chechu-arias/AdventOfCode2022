
n_overlap = 0
n_contained = 0
with open("input_d4.txt", "r") as f:

    section_assignments = f.readlines()
    for assignment in section_assignments:
        section_pair = assignment.split(",")
        first, second = section_pair[0].split("-"), section_pair[1].split("-")
        first_lower, first_upper = int(first[0]), int(first[1])
        second_lower, second_upper = int(second[0]), int(second[1])

        if first_lower <= second_lower and first_upper >= second_upper:
            n_contained += 1
        elif second_lower <= first_lower and second_upper >= first_upper:
            n_contained += 1

        if second_lower <= first_lower <= second_upper:
            n_overlap += 1
        elif first_lower <= second_lower <= first_upper:
            n_overlap += 1

print(f"The number of pairs where one contains the other is of {n_contained}.")
print(f"The number of pairs where there's an overlap is of {n_overlap}.")
