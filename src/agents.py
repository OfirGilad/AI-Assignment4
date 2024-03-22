from state import State
from utility_of_states import UtilityOfStates


class Agent:
    def __init__(self, state: State, utility_of_states: UtilityOfStates):
        self.state = state
        self.utility_of_states = utility_of_states
        self.agent_idx = state.agent_idx

    def perform_action(self):
        # Update agent picked and delivered packages
        self.state.update_agent_packages_status()
        agent_data = self.state.agents[self.agent_idx]
        action = self.utility_of_states.policy_next_step(state=self.state)

        action_name = self.state.perform_agent_action(
            current_vertex=agent_data["location"],
            action=action,
            mode="Coords"
        )
        self.state.update_agent_packages_status()
        return self.state, action_name
