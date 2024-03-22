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
