from state import State
from state_utility import StateUtility

import itertools
import numpy as np


class UtilityOfStates:
    def __init__(self, initial_state: State):
        self.initial_state = initial_state
        self.unknown_edges = list(edge for edge in self.initial_state.special_edges if edge["type"] == "fragile")
        self.states_utilities = dict()

    def _set_default_values(self):
        X = self.initial_state.X
        Y = self.initial_state.Y
        all_vertices = list(list(vertex) for vertex in itertools.product(range(X), range(Y)))
        for vertex in all_vertices:
            self.states_utilities[str(vertex)] = StateUtility(
                location=vertex,
                unknown_edges=self.unknown_edges,
                initial_value=np.inf
            )

    # TODO: Implement this method
    def preform_value_iteration(self):
        self._set_default_values()

        start_location = self.initial_state.agents[self.initial_state.agent_idx]["location"]
        goal_location = self.initial_state.picked_packages[0]["deliver_to"]

        # Set goal state utility
        self.states_utilities[str(goal_location)].set_utility_value(
            unknowns_state=["X"] * len(self.unknown_edges),
            value=0.0,
            action="no-op"
        )

        print("TBD")

    # TODO: Implement this method
    def belief_states_values(self):
        belief_states_str = ""
        return belief_states_str

    # TODO: Implement this method
    def policy_next_step(self, state: State):
        action = "Left"
        return action
