
OUTCOMES_PART1 = {
    ("A", "X"): 1+3,
    ("A", "Y"): 2+6,
    ("A", "Z"): 3+0,
    ("B", "X"): 1+0,
    ("B", "Y"): 2+3,
    ("B", "Z"): 3+6,
    ("C", "X"): 1+6,
    ("C", "Y"): 2+0,
    ("C", "Z"): 3+3,
}

OUTCOMES_PART2 = {
    ("A", "X"): 3+0,
    ("A", "Y"): 1+3,
    ("A", "Z"): 2+6,
    ("B", "X"): 1+0,
    ("B", "Y"): 2+3,
    ("B", "Z"): 3+6,
    ("C", "X"): 2+0,
    ("C", "Y"): 3+3,
    ("C", "Z"): 1+6,
}

score_part1 = 0
score_part2 = 0
with open("input_d2.txt", "r") as f:
    for line in f:
        elems = line.split()
        score_part1 += OUTCOMES_PART1[(elems[0], elems[1])]
        score_part2 += OUTCOMES_PART2[(elems[0], elems[1])]

print(f"The total score for part 1 is of {score_part1}.")

print(f"The total score for part 2 is of {score_part2}.")
