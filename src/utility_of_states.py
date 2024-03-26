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
            unknown_state=["X"] * len(self.unknown_edges),
            value=0.0,
            action="no-op"
        )

    def _check_edge_state(self, fragile_edge, unknown_state):
        for idx, unknown_edge in enumerate(self.unknown_edges):
            if unknown_edge["from"] == fragile_edge["from"] and unknown_edge["to"] == fragile_edge["to"]:
                return unknown_state[idx], idx
            elif unknown_edge["from"] == fragile_edge["to"] and unknown_edge["to"] == fragile_edge["from"]:
                return unknown_state[idx], idx
            else:
                continue

        raise Exception("Edge not found in unknown edges (fragile edges)")

    def _update_utilities_under_unknown_state(self, unknown_state):
        possible_moves = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        success_update = True

        while success_update:
            success_update = False

            for vertex in self.states_utilities.keys():
                state_utility = self.states_utilities[vertex]
                curr_location = state_utility.location

                for possible_move in possible_moves:
                    new_location = [curr_location[0] + possible_move[0], curr_location[1] + possible_move[1]]

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
                        edge_state = "F"
                        edge_idx = None
                        if edge_type == "fragile":
                            fragile_edge = {"from": curr_location, "to": new_location}
                            edge_state, edge_idx = self._check_edge_state(
                                fragile_edge=fragile_edge,
                                unknown_state=unknown_state
                            )

                        # If the edge state is blocked, continue to the next move
                        if edge_state == "T":
                            continue
                        # If the edge state is unblocked, calculate the new value
                        elif edge_state == "F":
                            next_location_value, _ = (
                                self.states_utilities[str(new_location)].utility_value_and_action(
                                    unknown_state=unknown_state
                                )
                            )

                        # If the edge state is unknown, calculate the new value based on the probabilities
                        elif edge_state == "U":
                            p = self.unknown_edges[edge_idx]["p"]

                            # TODO: Find how to calculate the probabilities correctly (by taking min cost option)

                            # TODO: Edge is blocked (need to look for alternative paths)
                            unknown_state_t = deepcopy(unknown_state)
                            unknown_state_t[edge_idx] = "T"
                            next_location_value_t, _ = (
                                self.states_utilities[str(new_location)].utility_value_and_action(
                                    unknown_state=unknown_state_t
                                )
                            )

                            # Edge is passable
                            unknown_state_f = deepcopy(unknown_state)
                            unknown_state_f[edge_idx] = "F"
                            next_location_value_f, _ = (
                                self.states_utilities[str(new_location)].utility_value_and_action(
                                    unknown_state=unknown_state_f
                                )
                            )

                            next_location_value = p * next_location_value_t + (1 - p) * next_location_value_f
                        else:
                            raise Exception("Unknown edge state")

                        new_value = (-edge_cost) + next_location_value
                        action = self.state.get_action_name(
                            current_vertex=curr_location,
                            next_vertex=new_location,
                            mode="Coords"
                        )
                        update_result = state_utility.update_utility_value(
                            unknown_state=unknown_state,
                            value=new_value,
                            action=action
                        )
                        if update_result:
                            success_update = True
                    else:
                        continue

    # TODO: Implement this method
    def preform_value_iteration(self):
        # start_location = self.state.picked_packages[0]["package_at"]
        goal_location = self.state.picked_packages[0]["deliver_to"]

        # Set initial values
        self._set_initial_values(goal_location=goal_location)

        # Get all possible known states
        known_states = itertools.product(["F", "T"], repeat=len(self.unknown_edges))
        known_states = list(list(known_state) for known_state in known_states)

        # Update utilities under known states
        for known_state in known_states:
            self._update_utilities_under_unknown_state(unknown_state=known_state)

        # Get all possible unknown states
        unknown_states = itertools.product(["F", "T", "U"], repeat=len(self.unknown_edges))
        unknown_states = list(list(unknown_state) for unknown_state in unknown_states if "U" in unknown_state)
        unknown_states.sort(key=lambda x: x.count("U"))

        # Update utilities under unknown states
        for unknown_state in unknown_states:
            self._update_utilities_under_unknown_state(unknown_state=unknown_state)

    def belief_states_values(self):
        belief_states_str = "Belief States Values:\n"

        # Get all belief states
        unknown_states = itertools.product(["F", "T", "U"], repeat=len(self.unknown_edges))
        unknown_states = list(list(unknown_state) for unknown_state in unknown_states)
        # unknown_states = list(list(unknown_state) for unknown_state in unknown_states if "U" in unknown_state)
        # unknown_states.sort(key=lambda x: x.count("U"))

        # Loop over all vertices
        X = self.state.X
        Y = self.state.Y
        all_vertices = list(list(vertex) for vertex in itertools.product(range(X), range(Y)))
        for vertex in all_vertices:
            belief_states_str += f"Vertex {tuple(vertex)}:\n"
            for unknown_state in unknown_states:
                value, action = self.states_utilities[str(vertex)].utility_value_and_action(
                    unknown_state=unknown_state
                )
                action = "unreachable" if action is None else action
                belief_states_str += f"U{str(unknown_state)}={value}, Optimal Action: {action}\n"
            belief_states_str += "\n"

        return belief_states_str

    def get_initial_unknown_state(self):
        unknown_state = ["U"] * len(self.unknown_edges)
        return unknown_state

    def _scan_closest_unknown_edges(self, state: State, unknown_state: list):
        # No unknown edges
        if unknown_state.count("U") == 0:
            return unknown_state

        agent_location = state.agents[0]["location"]
        for edge_idx, edge in enumerate(self.unknown_edges):
            # Skip known edges
            if unknown_state[edge_idx] != "U":
                continue

            if edge["from"] == agent_location:
                edge_type, _ = state.get_edge_type_and_cost(
                    current_vertex=agent_location,
                    next_vertex=edge["to"],
                    mode="Coords"
                )
            elif edge["to"] == agent_location:
                edge_type, _ = state.get_edge_type_and_cost(
                    current_vertex=agent_location,
                    next_vertex=edge["from"],
                    mode="Coords"
                )
            else:
                continue

            if edge_type == "always blocked":
                unknown_state[edge_idx] = "T"
            else:
                unknown_state[edge_idx] = "F"

        return unknown_state

    # TODO: Implement this method
    def policy_next_step(self, state: State, unknown_state: list):
        unknown_state = self._scan_closest_unknown_edges(state=state, unknown_state=unknown_state)

        agent_location = state.agents[0]["location"]
        state_utility = self.states_utilities[str(agent_location)]
        _, action = state_utility.utility_value_and_action(unknown_state=unknown_state)

        return action, unknown_state
