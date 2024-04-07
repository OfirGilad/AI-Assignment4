import itertools
from typing import Callable


class StateUtility:
    def __init__(self, location: list, unknown_edges_func: Callable, initial_value=None):
        self.location = location
        self.unknown_edges_func = unknown_edges_func
        self.edge_states = ["T", "F", "U"]
        self.utilities = dict()

        self._set_initial_values(initial_value=initial_value)

    def _set_initial_values(self, initial_value):
        unknown_edges = self.unknown_edges_func()
        iter_product = itertools.product(self.edge_states, repeat=len(unknown_edges))
        for product in iter_product:
            product_str = str(list(product))
            self.utilities[product_str] = {
                "value": initial_value,
                "optimal_action": None,
            }

    @staticmethod
    def _compare_states_format(state1: list, state2: list):
        if len(state1) != len(state2):
            raise Exception("States must have same length")

        compare_result = True
        for idx in range(len(state1)):
            # Handle wildcard: X in [T,F,U]
            if state1[idx] == "X" or state2[idx] == "X":
                continue
            # Handle semi wildcard: K in [T,F]
            if (state1[idx] == "K" and state2[idx] != "U") or (state1[idx] != "U" and state2[idx] == "K"):
                continue
            # Handle direct compare
            if state1[idx] != state2[idx]:
                compare_result = False
        return compare_result

    def update_utility_value(self, unknown_state: list, value: float, action=None):
        success_update = False
        unknown_edges = self.unknown_edges_func()
        iter_product = itertools.product(self.edge_states, repeat=len(unknown_edges))
        for product in iter_product:
            product_lst = list(product)
            if self._compare_states_format(product_lst, unknown_state):
                product_str = str(product_lst)
                current_value = self.utilities[product_str]["value"]
                if current_value >= value:
                    # print(
                    #     f"Failed to update location '{self.location}' utility state '{product_str}': "
                    #     f"new value: {value}, current value: {current_value}."
                    # )
                    continue
                else:
                    self.utilities[product_str]["value"] = value
                    self.utilities[product_str]["optimal_action"] = action
                    success_update = True
            else:
                continue

        return success_update

    def utility_value_and_action(self, unknown_state: list):
        value = None
        action = None
        unknown_edges = self.unknown_edges_func()
        iter_product = itertools.product(self.edge_states, repeat=len(unknown_edges))
        for product in iter_product:
            product_lst = list(product)
            if self._compare_states_format(product_lst, unknown_state):
                product_str = str(product_lst)
                value = self.utilities[product_str]["value"]
                action = self.utilities[product_str]["optimal_action"]
                break

        if value is not None:
            return value, action
        else:
            raise ValueError(f"Unknown state '{unknown_state}' for location '{self.location}'")


if __name__ == '__main__':
    result1 = StateUtility._compare_states_format(state1=["X", "X", "X"], state2=["T", "F", "U"])
    result2 = StateUtility._compare_states_format(state1=["K", "K"], state2=["T", "F"])
    print(result1)
    print(result2)
