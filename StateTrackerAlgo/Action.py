from OutputParser import OutputParser
from tests.ComplexTestCases import ComplexTestCases
from pyperplan.pddl.parser import Parser
from pyperplan.pddl.pddl import Predicate
import os

class BadModelPrediction(Exception):
    def __init__(self, message="Model prediction does not work."):
        super().__init__(message)

class Action:
    def __init__(self, domain, problem, model_output, output_parser: OutputParser):
        #Action object that represents an action with its states
        self.domain = domain
        self.problem = problem
        self.pddl_parser = Parser(self.domain, self.problem)

        self._model_output = model_output
        self.output_parser = output_parser

        self.ignore_list = ['clear', 'handempty']
        #Add more here for more things to ignore.

    def retrieve_action(self, word_tolerance, line_tolerance):
        action0, action1 = self.output_parser.parse(self._model_output, word_tolerance, line_tolerance)
        action = {**action0, **action1}
        #Merges the pick and place dictionaries.
        return action

    def get_pyperplan_initial_state(self, ignore_list):
        #Basically just gets the start state
        domain_parsed = self.pddl_parser.parse_domain(True)
        problem_parsed = self.pddl_parser.parse_problem(domain_parsed, True)
        initial_state = problem_parsed.initial_state
        block_placement = self.parse_initial_state(initial_state, ignore_list)
        return block_placement

    def write_sol_file(self, output_path: str) -> None:
        assert os.path.exists(output_path), f"{output_path} does not exist."
        start_state = self.get_pyperplan_initial_state(self.ignore_list)
        action = self.retrieve_action(3, 3)
        #Word and line tolerance can both be tuned, but I think 4 is the upper bound of what they should.
        with open(output_path, 'w') as f:
            if action['pick'] == "None":
            # Check 'None'
                line0 = f""
                line1 = f"\n"
                f.write(line0)
                f.write(line1)
                pick_action = 'None'
                place_action = 'None'
                return None
            #Pick/Unstack
            if start_state[action['pick']] == 'table':
                line0 = f"(pick-up {action['pick']})"
                #Pick up if it is mapped to the table
                f.write(line0)
            else:
                line0 = f"(unstack {action['pick']} {start_state[action['pick']]})"
                #Unstack if it is mapped to another block.
                f.write(line0)
            #put-down/stack
            if action['place'] == 'table':
                line1 = f"(put-down {action['pick']})"
            else:
                line1 = f"(stack {action['pick']} {action['place']})"
        return None

    #Helper functions
    @staticmethod
    def parse_initial_state(initial_state: list, ignore: list):
        block_placement = {}
        for placement in initial_state:
            skip = Action.filter_ignore(placement, ignore)
            if skip:
                continue
            block_placement[tuple(placement.signature)] = placement.name
        print(type(block_placement))
        block_placement = Action.get_start_state(block_placement)
        block_placement = Action.extract_object(block_placement, ['red_block', 'blue_block', 'yellow_block'])
        print(f"BLOCK PLACEMENT: {block_placement}")
        return block_placement

    @staticmethod
    def filter_ignore(placement: Predicate, ignore_list: list):
        #If the placement type needs to be ignored, return true.
        if placement.name in ignore_list:
            return True
        return False

    @staticmethod
    def get_start_state(block_placement: dict):
        updated_block_placement = {}
        for key, value in block_placement.items():
            assert value is not None
            if value == 'ontable':
                updated_block_placement[key] = 'table'
            elif value == 'on':
                top_block, bottom_block = key
                updated_block_placement[top_block] = bottom_block
            else:
                return None
        return updated_block_placement

    @staticmethod
    def extract_object(block_placement, objects):
        updated_block_placement = {}
        for key, value in block_placement.items():
            key = [i for i in key if i is not None][0]
            if type(key) is tuple:
                key, _ = key
            else:
                pass
            if type(value) is tuple:
                value, _ = value
            else:
                pass
            for object in objects:
                if key in object:
                    updated_block_placement[object] = value
        return updated_block_placement


if __name__ == '__main__':
    op = OutputParser('../domain.pddl', '../problem.pddl', keyword1='table', keyaction1='pick', keyword2='red_block',
                      keyword3='yellow_block', keyword4='blue_block', keyword5='None', keyaction2='place')
    string = ComplexTestCases.TEST5.value
    act = Action('../domain.pddl', '../problem.pddl', string, op)
    hehe = act.retrieve_action(3 ,3)
    print(hehe)
    ignore = ['clear', 'handempty']
    pepe = act.get_pyperplan_initial_state(ignore)

