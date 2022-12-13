
def initialize_comparation(val1, val2):
    if len(val1) > len(val2):
        return -1
    elif len(val1) == len(val2):
        return 0
    else:
        return 1


def compare_values(val1, val2):

    if isinstance(val1, int) and isinstance(val2, int):

        if val1 < val2:
            return 1
        elif val1 == val2:
            return 0
        else:
            return -1

    elif isinstance(val1, list) and isinstance(val2, list):

        index_l1 = 0
        index_l2 = 0
        comparation = initialize_comparation(val1, val2)
        while index_l1 < len(val1) and index_l2 < len(val2):
            comparation = compare_values(val1[index_l1], val2[index_l2])
            if comparation != 0:
                return comparation
            index_l1 += 1
            index_l2 += 1

        if index_l1 == len(val1) and index_l2 < len(val2):
            return 1
        elif index_l1 == len(val1) and index_l2 == len(val2):
            return comparation
        else:
            return -1

    elif isinstance(val1, list) and isinstance(val2, int):

        val2 = [val2]

        index_l1 = 0
        index_l2 = 0
        comparation = initialize_comparation(val1, val2)
        while index_l1 < len(val1) and index_l2 < len(val2):
            comparation = compare_values(val1[index_l1], val2[index_l2])
            if comparation != 0:
                return comparation
            index_l1 += 1
            index_l2 += 1

        if index_l1 == len(val1) and index_l2 < len(val2):
            return 1
        elif index_l1 == len(val1) and index_l2 == len(val2):
            return comparation
        else:
            return -1

    elif isinstance(val1, int) and isinstance(val2, list):

        val1 = [val1]

        index_l1 = 0
        index_l2 = 0
        comparation = initialize_comparation(val1, val2)
        while index_l1 < len(val1) and index_l2 < len(val2):
            comparation = compare_values(val1[index_l1], val2[index_l2])
            if comparation != 0:
                return comparation
            index_l1 += 1
            index_l2 += 1

        if index_l1 == len(val1) and index_l2 < len(val2):
            return 1
        elif index_l1 == len(val1) and index_l2 == len(val2):
            return comparation
        else:
            return -1


with open("input_d13.txt", "r") as f:
    data = f.readlines()

    index = 0
    n_pair = 1
    sum_correct_order = 0
    all_packages = list()
    while index < len(data):

        left = eval(data[index])
        right = eval(data[index+1])
        all_packages.append(left)
        all_packages.append(right)

        res = compare_values(left, right)

        if res >= 0:
            sum_correct_order += n_pair

        n_pair += 1
        index += 3

    print(f"The sum of indexes of ordered pairs is {sum_correct_order}.")

    divider_pack_1 = [[2]]
    divider_pack_2 = [[6]]
    all_packages.append(divider_pack_1)
    all_packages.append(divider_pack_2)

    all_packages_ordered = [0 for i in range(len(all_packages))]
    for i in range(len(all_packages)):
        this_package_order = 0
        for j in range(len(all_packages)):
            res = compare_values(all_packages[i], all_packages[j])
            if res == -1:
                this_package_order += 1

        all_packages_ordered[this_package_order] = all_packages[i]

    dec_key = 1
    for index in range(len(all_packages_ordered)):
        pack = all_packages_ordered[index]
        if pack == divider_pack_1 or pack == divider_pack_2:
            dec_key *= (index+1)

    print(f"The decoder key is {dec_key}.")


