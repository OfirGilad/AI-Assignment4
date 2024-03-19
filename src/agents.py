from state import State


class Agent:
    def __init__(self, state: State):
        self.state = state
        self.agent_idx = state.agent_idx

    def perform_action(self):
        # Update agent picked and delivered packages
        self.state.update_agent_packages_status()
        agent_data = self.state.agents[self.agent_idx]
        policy = self.state.get_agent_policy()

        action_name = self.state.perform_agent_action(
            current_vertex=agent_data["location"],
            action=policy["action"],
            mode="Coords"
        )
        self.state.update_agent_packages_status()
        return self.state, action_name
