
CRT = ""
CRT_DRAWING_POS = 0
CYCLE = 0
REG_X = 1
SIGNAL_STRENGTH = 0
SIGNAL_STRENGTH_CYCLES = [20, 60, 100, 140, 180, 220]


def set_signal_strength():
    global CYCLE, REG_X, SIGNAL_STRENGTH
    if CYCLE in SIGNAL_STRENGTH_CYCLES:
        SIGNAL_STRENGTH += (CYCLE * REG_X)


def set_crt():
    global CYCLE, REG_X, CRT, CRT_DRAWING_POS

    values = [REG_X-1, REG_X, REG_X+1]

    if CRT_DRAWING_POS > 0 and CRT_DRAWING_POS % 40 == 0:
        CRT += "\n"

    if (CRT_DRAWING_POS % 40) in values:
        CRT += "#"
    else:
        CRT += "."

    CRT_DRAWING_POS += 1


def noop():
    global CYCLE
    CYCLE += 1
    set_signal_strength()
    set_crt()


def addx(x):
    global CYCLE, REG_X
    CYCLE += 1
    set_signal_strength()
    set_crt()
    CYCLE += 1
    set_signal_strength()
    set_crt()
    REG_X += x


with open("input_d10.txt", "r") as f:
    data = f.readlines()
    for line in data:
        line = line.rstrip().split(" ")

        if line[0] == "noop":
            noop()
        elif line[0] == "addx":
            addx(int(line[1]))

    print(f"The signal strength is {SIGNAL_STRENGTH}.")
    print("The CRT is:")
    print(CRT)
