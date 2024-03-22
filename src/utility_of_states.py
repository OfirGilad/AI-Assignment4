from state import State
from state_utility import StateUtility


class UtilityOfStates:
    def __init__(self, initial_state: State):
        self.initial_state = initial_state
        self.states_utilities = dict()

    # TODO: Implement this method
    def calculate_states_utilities(self):
        start_location = self.initial_state.agents[self.initial_state.agent_idx]["location"]
        goal_location = self.initial_state.picked_packages[0]["package_at"]
        unknown_edges = [edge for edge in self.initial_state.special_edges if edge["type"] == "fragile"]

        # Set goal state utility
        self.states_utilities[str(goal_location)] = StateUtility(
            location=goal_location,
            unknown_edges=unknown_edges,
            initial_value=0.0
        )

    # TODO: Implement this method
    def belief_states_values(self):
        belief_states_str = ""
        return belief_states_str

    # TODO: Implement this method
    def policy_next_step(self, state: State):
        action = "Left"
        return action
