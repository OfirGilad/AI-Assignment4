from state import State
from simulator import Simulator


class Interface:
    def __init__(self, initial_state: State):
        self.initial_state = initial_state
        self.graph_instance = None
        self.user_actions = {
            "0": self._print_belief_state,
            "1": self._generate_new_graph_instance,
            "2": self._run_simulator,
            "3": self._quit
        }

    def _print_belief_state(self):
        print("Belief state printed!")

    def _generate_new_graph_instance(self):
        self.graph_instance = self.initial_state.clone_state(agent_idx=self.initial_state.agent_idx)
        # TODO: Replace fragile edges with always blocked edges or normal edges (with probabilities)
        print("Instance generated!")

    def _run_simulator(self):
        if self.graph_instance is None:
            print("A graph instance must exists before running the simulator.")
        else:
            simulator = Simulator(initial_state=self.graph_instance)
            simulator.run()

    @staticmethod
    def _quit():
        exit()

    def run(self):
        user_information = (
            "Choose operation from the following options:\n"
            "0. Print the value of each belief-state, and the optimal action in that belief state, if it exists.\n"
            "1. Generate new graph instance.\n"
            "2. Run simulator (Prerequisite: a graph instance must exists).\n"
            "3. Quit.\n"
            "Your choice: "
        )

        while True:
            user_input = input(user_information)
            user_action = self.user_actions.get(user_input, None)
            if user_action is not None:
                user_action()
            else:
                print(f"Invalid input: {user_input}! Write either '0','1','2' or '3'. \n")
