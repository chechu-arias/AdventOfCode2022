
import re

if __name__ == "__main__":
    min_x = float('inf')
    max_x = float('-inf')
    min_type = ""
    max_type = ""
    sensor_col = []
    sensor_row = []
    beacon_col = []
    beacon_row = []
    with open("input_d15.txt", "r") as f:
        for line in f.readlines():
            line_to_process = line.rstrip()
            pattern = re.search(r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)",
                                line_to_process)

            [s_x, s_y, b_x, b_y] = [int(i) for i in pattern.groups()]

            distance_from_sensor_to_beacon = abs(s_x - b_x) + abs(s_y - b_y)
            min_beacon_coverage = s_x - distance_from_sensor_to_beacon
            max_beacon_coverage = s_x + distance_from_sensor_to_beacon

            if min_x > min_beacon_coverage:
                min_x = min_beacon_coverage
                min_type = "sensor"
            if min_x > b_x:
                min_x = b_x
                min_type = "beacon"
            if max_x < max_beacon_coverage:
                max_x = max_beacon_coverage
                max_type = "sensor"
            if max_x < b_x:
                max_x = b_x
                max_type = "beacon"

            sensor_col.append(s_x)
            sensor_row.append(s_y)
            beacon_col.append(b_x)
            beacon_row.append(b_y)

    actual_row = 2000000
    impossible_ranges = list()

    min_range = 0
    max_range = 4000000
    possible_rows_ranges = {i: list() for i in range(max_range)}

    for index in range(len(sensor_col)):

        print(f"Processing sensor {index+1}/{len(sensor_col)}.")

        s_row, s_col = sensor_row[index], sensor_col[index]
        b_row, b_col = beacon_row[index], beacon_col[index]
        distance_from_sensor_to_beacon = abs(s_row - b_row) + abs(s_col - b_col)

        upper_row = s_row - distance_from_sensor_to_beacon
        lower_row = s_row + distance_from_sensor_to_beacon

        growing = True
        left_col, right_col = s_col, s_col
        for i in range(upper_row, lower_row + 1):

            if i == s_row:
                growing = False

            # Part 1
            if actual_row == i:

                row_range = [max(min_x, left_col), min(max_x, right_col)]

                impossible_ranges.append(row_range)

                if len(impossible_ranges) > 1:

                    row_ranges = sorted(impossible_ranges)

                    total_range = []
                    actual_range = row_ranges[0]
                    for j in range(1, len(row_ranges)):
                        next_range = row_ranges[j]
                        if (actual_range[1] + 1) >= next_range[0]:
                            actual_range = [actual_range[0], max(actual_range[1], next_range[1])]
                        else:
                            total_range.append(actual_range)
                            actual_range = next_range

                    total_range.append(actual_range)

                    impossible_ranges = total_range

            # Part 2
            if min_range <= i <= max_range and i in possible_rows_ranges:

                row_range = [max(min_range, left_col), min(max_range, right_col)]

                possible_rows_ranges[i].append(row_range)

                if i in possible_rows_ranges and len(possible_rows_ranges[i]) > 1:

                    row_ranges = possible_rows_ranges[i]
                    row_ranges = sorted(row_ranges)

                    total_range = []
                    actual_range = row_ranges[0]
                    for j in range(1, len(row_ranges)):
                        next_range = row_ranges[j]
                        if (actual_range[1] + 1) >= next_range[0]:
                            actual_range = [actual_range[0], max(actual_range[1], next_range[1])]
                        else:
                            total_range.append(actual_range)
                            actual_range = next_range

                    total_range.append(actual_range)

                    if len(total_range) == 1 and total_range[0] == [min_range, max_range]:
                        del possible_rows_ranges[i]
                    else:
                        possible_rows_ranges[i] = total_range

            if growing:
                left_col -= 1
                right_col += 1
            else:
                left_col += 1
                right_col -= 1

    n_impossible = 0
    for impossible_range in impossible_ranges:
        n_impossible += impossible_range[1] - impossible_range[0]

    print(f"The number of impossible positions is of {n_impossible}.")

    print(possible_rows_ranges)
    tuning_freq = 0
    for k, v in possible_rows_ranges.items():
        tuning_freq = (v[0][1] + 1) * max_range + k

    print(f"The tuning frequency is of {tuning_freq}.")
