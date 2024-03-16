from state import State
from ascii_parser import Parser


def run(data_filepath: str):
    parser = Parser()
    environment_data = parser.parse_data(data_filepath=data_filepath)
    # print(environment_data)
    initial_state = State(environment_data=environment_data)


def main():
    # TODO: Fill the data_filepath parameter
    data_filepath = "../input/input.txt"
    run(data_filepath=data_filepath)


if __name__ == '__main__':
    main()
