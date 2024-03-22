from state import State
from ascii_parser import Parser
from utility_of_states import UtilityOfStates
from interface import Interface


def run(data_filepath: str):
    # Init Environment Data
    parser = Parser()
    environment_data = parser.parse_data(data_filepath=data_filepath)

    # Init State
    initial_state = State(environment_data=environment_data)
    initial_state.update_agent_packages_status()

    # Init Utility of States
    utility_of_states = UtilityOfStates(initial_state=initial_state)
    utility_of_states.preform_value_iteration()

    # Init Interface
    interface = Interface(initial_state=initial_state, utility_of_states=utility_of_states)
    interface.run()


def main():
    # TODO: Fill the data_filepath parameter
    data_filepath = "../input/input.txt"
    run(data_filepath=data_filepath)


if __name__ == '__main__':
    main()
