from state import State
from utility_of_states import UtilityOfStates
from simulator import Simulator

from random import choices


class Interface:
    def __init__(self, initial_state: State, utility_of_states: UtilityOfStates):
        self.initial_state = initial_state
        self.utility_of_states = utility_of_states
        self.graph_instance = None
        self.user_actions = {
            "0": self._print_belief_states_values,
            "1": self._generate_new_graph_instance,
            "2": self._run_simulator,
            "3": self._quit
        }

    def _print_belief_states_values(self):
        results = self.utility_of_states.belief_states_values()
        print(results)

    def _generate_new_graph_instance(self):
        self.graph_instance = self.initial_state.clone_state()

        # Replace fragile edges with always blocked edges or normal edges (based on probabilities)
        updated_special_edges = list()
        for special_edge in self.graph_instance.special_edges:
            if special_edge["type"] == "fragile":
                p = special_edge["p"]
                population = [True, False]
                weights = [p, 1-p]
                choice = choices(population=population, weights=weights)

                if choice[0]:
                    special_edge["type"] = "always blocked"
                    updated_special_edges.append(special_edge)
                else:
                    continue
            else:
                updated_special_edges.append(special_edge)

        self.graph_instance.special_edges = updated_special_edges
        print("Graph instance generated!")

    def _run_simulator(self):
        if self.graph_instance is None:
            print("A graph instance must exists before running the simulator.")
        else:
            simulator = Simulator(initial_state=self.graph_instance, utility_of_states=self.utility_of_states)
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
