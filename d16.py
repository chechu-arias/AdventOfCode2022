def compute_receive(valve_connections_dict):
    res = dict()
    for valve, connections in valve_connections_dict.items():
        for conn, dist in connections:
            if conn not in res:
                res[conn] = list()
            res[conn].append((valve, dist))
    return res


class Node:

    def __init__(self, your_minutes_left, elephant_minutes_left, total_release_pressure, your_actual_valve,
                 elephant_actual_valve, valves_opened, history) -> None:

        self.your_minutes_left = your_minutes_left
        self.elephant_minutes_left = elephant_minutes_left
        self.total_release_pressure = total_release_pressure
        self.your_actual_valve = your_actual_valve
        self.elephant_actual_valve = elephant_actual_valve
        self.valves_opened = valves_opened
        self.history = history

    def __repr__(self) -> str:
        return f"{self.your_minutes_left} - {self.total_release_pressure} - {self.your_actual_valve} - {self.history}"

    def get_string(self) -> str:
        return f"{self.total_release_pressure} - {self.your_actual_valve} - {self.history}"

    def compute_max_pressure_ideal(self, valve_pressures_dict):
        approximation = 0
        your_minutes_left_now = self.your_minutes_left
        elephant_minutes_left_now = self.elephant_minutes_left

        valve_pressures_dict = {k: v for k, v in sorted(
            valve_pressures_dict.items(), key=lambda item: item[1], reverse=True)}

        for valve_name, pressure in valve_pressures_dict.items():

            if your_minutes_left_now >= elephant_minutes_left_now:

                if valve_name not in self.valves_opened and your_minutes_left_now > 0:
                    approximation += (pressure * (your_minutes_left_now - 1))
                    your_minutes_left_now -= 2

            else:

                if valve_name not in self.valves_opened and elephant_minutes_left_now > 0:
                    approximation += (pressure * (elephant_minutes_left_now - 1))
                    elephant_minutes_left_now -= 2

            # if valve_name not in self.valves_opened and minutes_left_now > 0:
            #     approximation += (pressure * (minutes_left_now - 1))
            #     minutes_left_now -= 2

        return self.total_release_pressure + approximation

    def explore_you(self, valve_pressures_dict, valve_connections_dict):
        options = list()

        if self.your_minutes_left == 0:
            return []

        if self.your_actual_valve not in self.valves_opened and valve_pressures_dict[self.your_actual_valve] > 0:
            actual_valves_opened = self.valves_opened.copy()
            actual_valves_opened.add(self.your_actual_valve)

            history_now = self.history.copy()
            history_now.append((f"YOU: Open {self.your_actual_valve}", self.your_minutes_left))

            options.append(
                Node(
                    self.your_minutes_left - 1,
                    self.elephant_minutes_left,
                    self.total_release_pressure + (valve_pressures_dict[self.your_actual_valve] * (self.your_minutes_left - 1)),
                    self.your_actual_valve,
                    self.elephant_actual_valve,
                    actual_valves_opened,
                    history_now
                )
            )

        connections = valve_connections_dict[self.your_actual_valve]
        for conn, conn_dist in connections:

            if valve_pressures_dict[conn] > 0 and conn not in self.valves_opened and self.your_minutes_left >= (
                    conn_dist + 1):

                actual_valves_opened = self.valves_opened.copy()
                actual_valves_opened.add(conn)

                history_now = self.history.copy()
                history_now.append((f"YOU: Move and open {conn}", self.your_minutes_left))

                options.append(
                    Node(
                        self.your_minutes_left - conn_dist - 1,
                        self.elephant_minutes_left,
                        self.total_release_pressure + (
                                    valve_pressures_dict[conn] * (self.your_minutes_left - conn_dist - 1)),
                        conn,
                        self.elephant_actual_valve,
                        actual_valves_opened,
                        history_now
                    )
                )

            elif self.your_minutes_left >= conn_dist:

                history_now = self.history.copy()
                history_now.append((f"YOU: Move {conn}", self.your_minutes_left))

                options.append(
                    Node(
                        self.your_minutes_left - conn_dist,
                        self.elephant_minutes_left,
                        self.total_release_pressure,
                        conn,
                        self.elephant_actual_valve,
                        self.valves_opened.copy(),
                        history_now
                    )
                )

        return options

    def explore_elephant(self, valve_pressures_dict, valve_connections_dict):
        options = list()

        if self.elephant_minutes_left == 0:
            return []

        if self.elephant_actual_valve not in self.valves_opened and \
                valve_pressures_dict[self.elephant_actual_valve] > 0:

            actual_valves_opened = self.valves_opened.copy()
            actual_valves_opened.add(self.elephant_actual_valve)

            history_now = self.history.copy()
            history_now.append((f"ELEPHANT: Open {self.elephant_actual_valve}", self.elephant_minutes_left))

            options.append(
                Node(
                    self.your_minutes_left,
                    self.elephant_minutes_left - 1,
                    self.total_release_pressure +
                    (valve_pressures_dict[self.elephant_actual_valve] * (self.elephant_minutes_left - 1)),
                    self.your_actual_valve,
                    self.elephant_actual_valve,
                    actual_valves_opened,
                    history_now
                )
            )

        connections = valve_connections_dict[self.elephant_actual_valve]
        for conn, conn_dist in connections:

            if valve_pressures_dict[conn] > 0 and conn not in self.valves_opened and self.elephant_minutes_left >= (
                    conn_dist + 1):

                actual_valves_opened = self.valves_opened.copy()
                actual_valves_opened.add(conn)

                history_now = self.history.copy()
                history_now.append((f"ELEPHANT: Move and open {conn}", self.elephant_minutes_left))

                options.append(
                    Node(
                        self.your_minutes_left,
                        self.elephant_minutes_left - conn_dist - 1,
                        self.total_release_pressure + (
                                    valve_pressures_dict[conn] * (self.elephant_minutes_left - conn_dist - 1)),
                        self.your_actual_valve,
                        conn,
                        actual_valves_opened,
                        history_now
                    )
                )

            elif self.elephant_minutes_left >= conn_dist:

                history_now = self.history.copy()
                history_now.append((f"ELEPHANT: Move {conn}", self.elephant_minutes_left))

                options.append(
                    Node(
                        self.your_minutes_left,
                        self.elephant_minutes_left - conn_dist,
                        self.total_release_pressure,
                        self.your_actual_valve,
                        conn,
                        self.valves_opened.copy(),
                        history_now
                    )
                )

        return options


if __name__ == "__main__":

    valve_pressures_dict = dict()
    valve_connections_dict = dict()
    with open("input_d16.txt", "r") as f:
        for line in f.readlines():
            line_to_process = line.rstrip()

            line_elements = line.split(";")

            valve_definition = line_elements[0]

            valve_name = valve_definition.split(" ")[1]
            valve_pressure = valve_definition.split("=")[-1]

            valve_pressures_dict[valve_name] = int(valve_pressure)

            valve_connections = line_elements[1].strip().split(", ")
            valve_connections[0] = valve_connections[0].split(" ")[-1]
            valve_connections_dist = list()
            for valve_conn in valve_connections:
                valve_connections_dist.append((valve_conn, 1))
            valve_connections_dict[valve_name] = valve_connections_dist

    starting_valve = "AA"
    valve_receive_dict = compute_receive(valve_connections_dict)

    for valve, valve_pressure in valve_pressures_dict.items():
        if valve_pressure == 0 and valve != starting_valve:

            for receive_valve, receive_valve_dist in valve_receive_dict[valve]:

                # Add valves that valve removed reached
                for conn_valve, conn_valve_dist in valve_connections_dict[valve]:
                    if conn_valve != receive_valve:
                        valve_connections_dict[receive_valve].append((conn_valve, receive_valve_dist + conn_valve_dist))

                # Remove valve that we want to remove
                aux = list()
                for conn_valve, conn_valve_dist in valve_connections_dict[receive_valve]:
                    if conn_valve != valve:
                        aux.append((conn_valve, conn_valve_dist))

                valve_connections_dict[receive_valve] = aux

            valve_connections_dict.pop(valve)
            valve_receive_dict = compute_receive(valve_connections_dict)

    valve_pressures_dict_final = valve_pressures_dict.copy()
    for valve in valve_pressures_dict.keys():
        if valve not in valve_connections_dict:
            del valve_pressures_dict_final[valve]

    valve_pressures_dict = valve_pressures_dict_final

    starting_node = Node(30, 0, 0, "AA", "AA", set(), list())
    candidates = [starting_node]
    best_global_node = None
    maximum_pressure_released = 0

    n_iters = 0
    while candidates:

        best_candidate = candidates.pop(0)

        options = best_candidate.explore_you(valve_pressures_dict, valve_connections_dict)

        best_node = None
        max_release = float('-inf')
        for option in options:

            if option.total_release_pressure > max_release:
                best_node = option
                max_release = option.total_release_pressure

        if best_node is not None and best_node.total_release_pressure > maximum_pressure_released:
            maximum_pressure_released = best_node.total_release_pressure
            best_global_node = best_node

        for option in options:
            if option.compute_max_pressure_ideal(valve_pressures_dict) >= maximum_pressure_released:
                candidates.append(option)

        n_iters += 1

    print(maximum_pressure_released, best_global_node.valves_opened)
    print(best_global_node.history)
    print(f"After {n_iters} iterations, most released pressure in part 1 is of {maximum_pressure_released}.")

    starting_node = Node(26, 26, 0, "AA", "AA", set(), list())
    candidates = [starting_node]
    best_global_node = None
    maximum_pressure_released = 0

    n_iters = 0
    while candidates:

        best_candidate = candidates.pop(0)

        if n_iters > 0 and n_iters % 100_000 == 0:
            print(n_iters, len(candidates))

        options = best_candidate.explore_you(valve_pressures_dict, valve_connections_dict)
        options = [item for op in options for item in op.explore_elephant(valve_pressures_dict, valve_connections_dict)]

        best_node = None
        max_release = float('-inf')
        for option in options:

            if option.total_release_pressure > max_release:
                best_node = option
                max_release = option.total_release_pressure

        if best_node is not None and best_node.total_release_pressure > maximum_pressure_released:
            maximum_pressure_released = best_node.total_release_pressure
            best_global_node = best_node

        for option in options:
            if option.compute_max_pressure_ideal(valve_pressures_dict) >= maximum_pressure_released:
                candidates.append(option)

        n_iters += 1

    print(maximum_pressure_released, best_global_node.valves_opened)
    print(best_global_node.history)
    print(f"After {n_iters} iterations, most released pressure in part 2 is of {maximum_pressure_released}.")
