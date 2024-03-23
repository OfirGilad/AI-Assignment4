import itertools


class StateUtility:
    def __init__(self, location: list, unknown_edges: list, initial_value=None):
        self.location = location
        self.unknown_edges = unknown_edges
        self.edges_states = ["T", "F", "U"]
        self.utilities = dict()

        self._set_initial_values(initial_value=initial_value)

    def _set_initial_values(self, initial_value):
        iter_product = itertools.product(self.edges_states, repeat=len(self.unknown_edges))
        for product in iter_product:
            product_str = str(list(product))
            self.utilities[product_str] = {
                "value": initial_value,
                "optimal_action": None,
            }

    @staticmethod
    def _compare_states_format(state1: list, state2: list):
        for idx, edge in enumerate(state1):
            if edge == "X" or state2[idx] == "X":
                continue
            if edge != state2[idx]:
                return False
        return True

    def update_utility_value(self, unknowns_state: list, value: float, action=None):
        success_update = False
        iter_product = itertools.product(self.edges_states, repeat=len(self.unknown_edges))
        for product in iter_product:
            product_lst = list(product)
            if self._compare_states_format(product_lst, unknowns_state):
                product_str = str(product_lst)
                curr_value = self.utilities[product_str]["value"]
                if curr_value >= value:
                    print(
                        f"Failed to update location '{self.location}' utility state '{product_str}': "
                        f"new value: {value}, current value: {curr_value}."
                    )
                else:
                    self.utilities[product_str]["value"] = value
                    self.utilities[product_str]["optimal_action"] = action
                    success_update = True
            else:
                continue

        return success_update

    def utility_value(self, unknowns_state: list):
        value = None
        iter_product = itertools.product(self.edges_states, repeat=len(self.unknown_edges))
        for product in iter_product:
            product_lst = list(product)
            if self._compare_states_format(product_lst, unknowns_state):
                product_str = str(product_lst)
                value = self.utilities[product_str]["value"]
                break

        if value is not None:
            return value
        else:
            raise ValueError(f"Unknown state '{unknowns_state}' for location '{self.location}'")


if __name__ == '__main__':
    result = StateUtility._compare_states_format(state1=["X", "X", "X"], state2=["T", "F", "U"])
    print(result)
