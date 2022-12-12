
from math import gcd


def multiply(x, y):
    return x * y


def add(x, y):
    return x + y


class Monkey:
    monkey_id = -1
    items = list()
    n_test = -1
    true_throw_index = -1
    false_throw_index = -1

    def __init__(self, monkey_id, initial_items, operator, y, n_test, true_throw, false_throw):
        self.monkey_id = monkey_id
        self.items = initial_items
        self.operator = operator
        self.y_value = y
        self.n_test = n_test
        self.true_throw_index = true_throw
        self.false_throw_index = false_throw

    def passes_test(self, worry_level):
        return (worry_level % self.n_test) == 0

    def get_worry_level(self, worry_level):
        if isinstance(self.y_value, int):
            return self.operator(worry_level, self.y_value)
        else:
            return self.operator(worry_level, worry_level)


def get_input():

    with open("input_d11.txt", "r") as f:

        data = f.readlines()

        index = 0
        monkeys = list()
        n_tests = list()
        while index < len(data):

            line = data[index].rstrip().split(" ")[1]
            monkey_id = int(line.replace(":", ""))
            index += 1
            items_line = data[index].rstrip().split(":")[1].replace(" ", "").split(",")
            monkey_items = [int(x) for x in items_line]
            index += 1
            operation_line = data[index].rstrip().split(":")[1].strip().split(" ")

            operation, operation_y = operation_line[3], operation_line[4]
            if operation_y.isnumeric():
                operation_y = int(operation_y)
            else:
                operation_y = operation_y

            if operation == "+":
                monkey_operation = add
            elif operation == "*":
                monkey_operation = multiply
            else:
                raise Exception

            index += 1
            n_test = int(data[index].rstrip().split(" ")[-1])

            index += 1
            true_test = int(data[index].rstrip().split(" ")[-1])

            index += 1
            false_test = int(data[index].rstrip().split(" ")[-1])

            if true_test == monkey_id or false_test == monkey_id:
                raise Exception

            m = Monkey(monkey_id, monkey_items, monkey_operation, operation_y, n_test, true_test, false_test)

            monkeys.append(m)
            n_tests.append(n_test)

            index += 2
    return monkeys, n_tests


monkeys, _ = get_input()

counts = [0 for i in range(len(monkeys))]
for i in range(20):
    for m in monkeys:
        counts[m.monkey_id] += len(m.items)
        for item in m.items:
            item_worry_level = m.get_worry_level(item) // 3
            if m.passes_test(item_worry_level):
                monkeys[m.true_throw_index].items.append(item_worry_level)
            else:
                monkeys[m.false_throw_index].items.append(item_worry_level)
        m.items = list()

two_most_active = [-1, -1]
for c in counts:
    if c > two_most_active[0]:
        two_most_active[1] = two_most_active[0]
        two_most_active[0] = c
    elif c > two_most_active[1]:
        two_most_active[1] = c

monkey_business = two_most_active[0] * two_most_active[1]

print(f"The monkey bussiness for part 1 is of {monkey_business}.")

monkeys, n_tests = get_input()

lcm = 1
for i in n_tests:
    lcm = lcm * i // gcd(lcm, i)

counts = [0 for i in range(len(monkeys))]
for i in range(10000):
    for m in monkeys:
        counts[m.monkey_id] += len(m.items)
        for item in m.items:
            item_worry_level = m.get_worry_level(item)
            if m.passes_test(item_worry_level):
                monkeys[m.true_throw_index].items.append((item_worry_level % lcm))
            else:
                monkeys[m.false_throw_index].items.append((item_worry_level % lcm))
        m.items = list()

two_most_active = [-1, -1]
for c in counts:
    if c > two_most_active[0]:
        two_most_active[1] = two_most_active[0]
        two_most_active[0] = c
    elif c > two_most_active[1]:
        two_most_active[1] = c

monkey_business = two_most_active[0] * two_most_active[1]

print(f"The monkey bussiness for part 2 is of {monkey_business}.")
