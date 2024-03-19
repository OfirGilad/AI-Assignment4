from agents import Agent
from state import State


class Simulator:
    def __init__(self, initial_state: State):
        self.current_state = initial_state
        self.states = [self.current_state]

    def _goal_achieved(self):
        goal_validation = (
            len(self.current_state.packages) == 0 and
            len(self.current_state.placed_packages) == 0 and
            len(self.current_state.picked_packages) == 0
        )
        if goal_validation:
            print("Goal achieved: All available packages have been delivered or disappeared")
            print(f"Final State:")
            print(self.current_state)
            return True
        else:
            return False

    def run(self):
        agent_idx = 0
        print("# Clock Time 0.0:")

        # Check if goal achieved
        if self._goal_achieved():
            return

        while True:
            # Perform Agent Action
            self.current_state = self.current_state.clone_state(agent_idx=agent_idx)
            current_agent = Agent(state=self.current_state)
            self.current_state, action = current_agent.perform_action()
            self.states.append(self.current_state)

            # Print Agent Action
            agent_type = self.current_state.agents[agent_idx]['type']
            print(f"Agent {agent_idx} ({agent_type}) Action: {action}")

            # Raise clock by one
            self.current_state = self.current_state.clone_state(agent_idx=agent_idx, time_factor=1)
            self.current_state.update_packages_info()
            print(f"# Clock Time {self.current_state.time}:")

            # Check if goal achieved
            if self._goal_achieved():
                return
