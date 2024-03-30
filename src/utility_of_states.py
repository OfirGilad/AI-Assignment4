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

        self.unknown_edges = [edge for edge in self.state.special_edges if edge["type"] == "fragile"]
        self.unknown_edges_func = lambda: self.unknown_edges
        self.states_utilities = dict()

        self.all_packages = (
            self.state.packages +
            self.state.picked_packages +
            self.state.placed_packages +
            self.state.archived_packages
        )

    def _set_initial_values(self, goal_location):
        X = self.state.X
        Y = self.state.Y
        all_vertices = [list(vertex) for vertex in itertools.product(range(X), range(Y))]
        for vertex in all_vertices:
            self.states_utilities[str(vertex)] = StateUtility(
                location=vertex,
                unknown_edges_func=self.unknown_edges_func,
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

    def _find_alternative_new_locations(self, curr_location, current_move, unknown_state):
        possible_moves = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        alternative_new_locations = list()

        for alternative_move in possible_moves:
            if alternative_move == current_move:
                continue

            new_location = [curr_location[0] + alternative_move[0], curr_location[1] + alternative_move[1]]

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
                if edge_type == "fragile":
                    fragile_edge = {"from": curr_location, "to": new_location}
                    edge_state, _ = self._check_edge_state(
                        fragile_edge=fragile_edge,
                        unknown_state=unknown_state
                    )

                if edge_state == "T":
                    continue
                elif edge_state == "F":
                    alternative_new_locations.append(new_location)
                elif edge_state == "U":
                    continue

        return alternative_new_locations

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
                            ###################
                            # Edge is blocked #
                            ###################
                            unknown_state_t = deepcopy(unknown_state)
                            unknown_state_t[edge_idx] = "T"
                            alternative_new_locations = self._find_alternative_new_locations(
                                curr_location=curr_location,
                                current_move=possible_move,
                                unknown_state=unknown_state_t
                            )

                            # If there are no alternative new locations, continue to the next move
                            if len(alternative_new_locations) == 0:
                                continue
                            # If there are alternative new locations, calculate the new value based on the maximum value
                            else:
                                min_path_cost = -np.inf
                                for alternative_new_location in alternative_new_locations:
                                    alternative_location_value, _ = (
                                        self.states_utilities[str(alternative_new_location)].utility_value_and_action(
                                            unknown_state=unknown_state_t
                                        )
                                    )
                                    min_path_cost = max(min_path_cost, alternative_location_value)
                                next_location_value_t = min_path_cost

                            #####################
                            # Edge is unblocked #
                            #####################
                            unknown_state_f = deepcopy(unknown_state)
                            unknown_state_f[edge_idx] = "F"
                            next_location_value_f, _ = (
                                self.states_utilities[str(new_location)].utility_value_and_action(
                                    unknown_state=unknown_state_f
                                )
                            )

                            p = self.unknown_edges[edge_idx]["p"]
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

    def preform_value_iteration(self):
        goal_location = self.all_packages[0]["deliver_to"]

        # Set initial values
        self._set_initial_values(goal_location=goal_location)

        # Get all possible known states
        known_states = itertools.product(["F", "T"], repeat=len(self.unknown_edges))
        known_states = [list(known_state) for known_state in known_states]

        # Update utilities under known states
        for known_state in known_states:
            self._update_utilities_under_unknown_state(unknown_state=known_state)

        # Get all possible unknown states
        unknown_states = itertools.product(["F", "T", "U"], repeat=len(self.unknown_edges))
        unknown_states = [list(unknown_state) for unknown_state in unknown_states if "U" in unknown_state]
        unknown_states.sort(key=lambda x: x.count("U"))

        # Update utilities under unknown states
        for unknown_state in unknown_states:
            self._update_utilities_under_unknown_state(unknown_state=unknown_state)

    def belief_states_values(self):
        belief_states_str = "Belief States Values:\n"

        # Get all belief states
        unknown_states = itertools.product(["F", "T", "U"], repeat=len(self.unknown_edges))
        unknown_states = [list(unknown_state) for unknown_state in unknown_states]

        # # Filter belief states with unknown edges
        # unknown_states = [list(unknown_state) for unknown_state in unknown_states if "U" in unknown_state]
        # unknown_states.sort(key=lambda x: x.count("U"))

        # Loop over all vertices
        X = self.state.X
        Y = self.state.Y
        all_vertices = [list(vertex) for vertex in itertools.product(range(X), range(Y))]
        for vertex in all_vertices:
            belief_states_str += "\n"
            belief_states_str += f"Vertex {tuple(vertex)}:\n"
            for unknown_state in unknown_states:
                value, action = self.states_utilities[str(vertex)].utility_value_and_action(
                    unknown_state=unknown_state
                )
                action = "unreachable" if action is None else action
                belief_states_str += f"  U{str(unknown_state)}={value}, Optimal Action: {action}\n"

        return belief_states_str

    def get_initial_unknown_state(self):
        unknown_state = ["U"] * len(self.unknown_edges)
        return unknown_state

    def _scan_closest_fragile_edges(self, current_location: list, unknown_state: list):
        closest_not_scanned_edges_indices = list()

        # No unknown edges
        if unknown_state.count("U") == 0:
            return closest_not_scanned_edges_indices, unknown_state

        for edge_idx, edge in enumerate(self.unknown_edges):
            if unknown_state[edge_idx] != "U":
                continue

            if edge["from"] == current_location:
                closest_not_scanned_edges_indices.append(edge_idx)
                unknown_state[edge_idx] = "X"
            elif edge["to"] == current_location:
                closest_not_scanned_edges_indices.append(edge_idx)
                unknown_state[edge_idx] = "X"
            else:
                continue
        return closest_not_scanned_edges_indices, unknown_state

    def _find_policy_recursive(self,
                               current_location: list,
                               goal_location: list,
                               unknown_state: list,
                               bulk_format: str,
                               path_cost: int,
                               policy_str: str):
        if current_location == goal_location:
            policy_str += f"{bulk_format} Action: 'no-op', Path cost: {path_cost} (Goal reached)\n"
        else:
            closest_not_scanned_edges_indices, unknown_state = self._scan_closest_fragile_edges(
                current_location=current_location,
                unknown_state=unknown_state
            )
            if len(closest_not_scanned_edges_indices) == 0:
                state_utility = self.states_utilities[str(current_location)]
                expected_value, action = state_utility.utility_value_and_action(unknown_state=unknown_state)
                if action is None:
                    policy_str += (
                        f"{bulk_format} Action: 'no-op', Path cost: -inf "
                        f"(Goal might be unreachable and it's best to stop)\n"
                    )
                else:
                    move = self.state.convert_action_to_movement(action=action)
                    next_location = [current_location[0] + move[0], current_location[1] + move[1]]

                    from_coords = f"({current_location[0]},{current_location[1]})"
                    to_coords = f"({next_location[0]},{next_location[1]})"
                    policy_str += f"{bulk_format} Action: '{action}' (From '{from_coords}' to '{to_coords}')\n"

                    policy_str = self._find_policy_recursive(
                        current_location=next_location,
                        goal_location=goal_location,
                        unknown_state=unknown_state,
                        bulk_format=bulk_format,
                        path_cost=path_cost-1,
                        policy_str=policy_str
                    )
            else:
                edges_states_combinations = itertools.product(["F", "T"], repeat=len(closest_not_scanned_edges_indices))
                edges_states_combinations = [list(combination) for combination in edges_states_combinations]

                for combination in edges_states_combinations:
                    policy_str += f"{bulk_format} If ("
                    combination_unknown_state = deepcopy(unknown_state)
                    separator = ""
                    for idx, edge_idx in enumerate(closest_not_scanned_edges_indices):
                        edge = self.unknown_edges[edge_idx]
                        edge_identifier = edge["identifier"]
                        policy_str += f"{separator}Blocked['{edge_identifier}']={combination[idx]}"
                        separator = " and "
                        combination_unknown_state[edge_idx] = combination[idx]
                    policy_str += "):\n"

                    policy_str = self._find_policy_recursive(
                        current_location=current_location,
                        goal_location=goal_location,
                        unknown_state=combination_unknown_state,
                        bulk_format=f"{bulk_format}{bulk_format}",
                        path_cost=path_cost,
                        policy_str=policy_str
                    )

        return policy_str

    def find_policy(self):
        policy_str = "The Constructed Policy:\n\n"

        start_location = self.all_packages[0]["package_at"]
        goal_location = self.all_packages[0]["deliver_to"]
        unknown_state = self.get_initial_unknown_state()
        bulk_format = "->"
        path_cost = 0

        policy_str = self._find_policy_recursive(
            current_location=deepcopy(start_location),
            goal_location=goal_location,
            unknown_state=deepcopy(unknown_state),
            bulk_format=bulk_format,
            path_cost=path_cost,
            policy_str=policy_str
        )

        state_utility = self.states_utilities[str(start_location)]
        expected_value, action = state_utility.utility_value_and_action(unknown_state=unknown_state)
        policy_str += f"Policy Expected Utility: {expected_value}\n"

        return policy_str

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

    def policy_next_step(self, state: State, unknown_state: list):
        unknown_state = self._scan_closest_unknown_edges(state=state, unknown_state=unknown_state)

        agent_location = state.agents[0]["location"]
        state_utility = self.states_utilities[str(agent_location)]
        _, action = state_utility.utility_value_and_action(unknown_state=unknown_state)

        return action, unknown_state
