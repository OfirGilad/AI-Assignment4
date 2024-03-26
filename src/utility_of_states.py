from state import State
from state_utility import StateUtility

import itertools
import numpy as np
from copy import deepcopy


class UtilityOfStates:
    def __init__(self, initial_state: State):
        # Remove agent location for checking available paths
        self.state = initial_state.clone_state()
        self.state.agents[0]["location"] = None

        self.unknown_edges = list(edge for edge in self.state.special_edges if edge["type"] == "fragile")
        self.states_utilities = dict()

    def _set_initial_values(self, goal_location):
        X = self.state.X
        Y = self.state.Y
        all_vertices = list(list(vertex) for vertex in itertools.product(range(X), range(Y)))
        for vertex in all_vertices:
            self.states_utilities[str(vertex)] = StateUtility(
                location=vertex,
                unknown_edges=self.unknown_edges,
                initial_value=-np.inf
            )

        # Set goal state utility
        self.states_utilities[str(goal_location)].update_utility_value(
            unknowns_state=["X"] * len(self.unknown_edges),
            value=0.0,
            action="no-op"
        )

    def _check_edge_state(self, fragile_edge, known_state):
        for idx, unknown_edge in enumerate(self.unknown_edges):
            if unknown_edge["from"] == fragile_edge["from"] and unknown_edge["to"] == fragile_edge["to"]:
                return known_state[idx]
            elif unknown_edge["from"] == fragile_edge["to"] and unknown_edge["to"] == fragile_edge["from"]:
                return known_state[idx]
            else:
                continue

        raise Exception("Edge not found in unknown edges (fragile edges)")

    def _update_utilities_under_known_states(self, known_state):
        possible_moves = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        success_update = True

        while success_update:
            success_update = False

            for vertex in self.states_utilities.keys():
                state_utility = self.states_utilities[vertex]
                curr_location = state_utility.location

                for move in possible_moves:
                    new_location = [curr_location[0] + move[0], curr_location[1] + move[1]]

                    # Validate if the new location is a vertex on the graph
                    try:
                        self.state.coordinates_to_vertex_index(coords=new_location)
                    except:
                        continue

                    if self.state.is_path_available(current_vertex=curr_location,
                                                    next_vertex=new_location,
                                                    mode="Coords"):
                        edge_type, edge_cost = self.state.get_edge_type_and_cost(
                            current_vertex=curr_location,
                            next_vertex=new_location,
                            mode="Coords"
                        )
                        if edge_type == "fragile":
                            fragile_edge = {"from": curr_location, "to": new_location}
                            state_value = self._check_edge_state(fragile_edge=fragile_edge, known_state=known_state)

                            # If the edge is blocked, continue to the next move
                            if state_value == "T":
                                continue

                        action = self.state.get_action_name(
                            current_vertex=curr_location,
                            next_vertex=new_location,
                            mode="Coords"
                        )
                        next_location_value = self.states_utilities[str(new_location)].utility_value(
                            unknowns_state=known_state
                        )
                        new_value = (-edge_cost) + next_location_value
                        update_result = state_utility.update_utility_value(
                            unknowns_state=known_state,
                            value=new_value,
                            action=action
                        )
                        if update_result:
                            success_update = True
                    else:
                        continue

    def _update_utilities_under_unknown_states(self):
        pass

    # TODO: Implement this method
    def preform_value_iteration(self):
        start_location = self.state.picked_packages[0]["package_at"]
        goal_location = self.state.picked_packages[0]["deliver_to"]

        # Set initial values
        self._set_initial_values(goal_location=goal_location)

        # Get all possible known states
        known_states = itertools.product(["F", "T"], repeat=len(self.unknown_edges))
        known_states = list(list(known_state) for known_state in known_states)

        # Update utilities under known states
        for known_state in known_states:
            self._update_utilities_under_known_states(known_state=known_state)

        # Get all possible unknown states
        unknown_states = itertools.product(["F", "T", "U"], repeat=len(self.unknown_edges)+1)
        unknown_states = list(list(unknown_state) for unknown_state in unknown_states if "U" in unknown_state)

        print("TBD")

    # TODO: Implement this method
    def belief_states_values(self):
        belief_states_str = ""
        return belief_states_str

    # TODO: Implement this method
    def policy_next_step(self, state: State):
        action = "Left"
        return action
