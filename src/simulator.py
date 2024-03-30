from agents import Agent
from state import State
from utility_of_states import UtilityOfStates


class Simulator:
    def __init__(self, initial_state: State, utility_of_states: UtilityOfStates):
        self.no_op_count = 0
        self.normal_agents_count = 1
        self.current_state = initial_state
        self.utility_of_states = utility_of_states
        self.unknown_state = self.utility_of_states.get_initial_unknown_state()
        # self.states = [self.current_state]

    def _goal_achieved(self):
        goal_validation1 = (
            len(self.current_state.packages) == 0 and
            len(self.current_state.placed_packages) == 0 and
            len(self.current_state.picked_packages) == 0
        )
        goal2_validation = (
            len(self.current_state.packages) == 0 and
            self.no_op_count == self.normal_agents_count
        )
        if goal_validation1:
            print("Goal achieved: All available packages have been delivered or disappeared")
            print(f"Final State:")
            print(self.current_state)
            return True
        elif goal2_validation:
            print(
                "Goal achieved: The agent performed no-op action \n"
                "(According to the policy the goal might be unreachable and it is better to stop the simulation)."
            )
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
            self.current_state = self.current_state.clone_state()
            current_agent = Agent(
                state=self.current_state,
                utility_of_states=self.utility_of_states,
                unknown_state=self.unknown_state
            )
            self.current_state, action = current_agent.perform_action()
            # self.states.append(self.current_state)

            # Print Agent Action
            agent_type = self.current_state.agents[agent_idx]['type']
            print(f"Agent {agent_idx} ({agent_type}) Action: {action}")
            if action == "no-op":
                self.no_op_count += 1

            # Raise clock by one
            self.current_state = self.current_state.clone_state(time_factor=1)
            self.current_state.update_packages_info()
            print(f"# Clock Time {self.current_state.time}:")

            # Check if goal achieved
            if self._goal_achieved():
                return

            # # Rest no-op actions
            # if agent_idx == 0:
            #     self.no_op_count = 0
