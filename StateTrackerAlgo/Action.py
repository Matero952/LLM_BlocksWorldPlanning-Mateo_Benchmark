from OutputParser import OutputParser
from tests.ComplexTestCases import ComplexTestCases
from pyperplan.pddl.parser import Parser
from pyperplan.pddl.pddl import Predicate


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
        self.start_state, self.end_state = None, None

    def retrieve_action(self, word_tolerance, line_tolerance):
        action = self.output_parser.parse(self._model_output, word_tolerance, line_tolerance)
        return action

    def retrieve_start_state(self):
        domain_parsed = self.pddl_parser.parse_domain(True)
        problem_parsed = self.pddl_parser.parse_problem(domain_parsed, True)
        initial_state = problem_parsed.initial_state
        print(f"Initial state: {initial_state}")
        print(f"Initial state type: {type(initial_state)}")
        print(self.parse_initial_state(initial_state))


    @staticmethod
    def parse_initial_state(initial_state: list):
        objects = []
        positions = []
        for placement in initial_state:
            assert type(placement) == Predicate, "Placement is not a Predicate"
            objects.append(placement.signature)
            positions.append(placement.name)
        return objects, positions




if __name__ == '__main__':
    op = OutputParser('../domain.pddl', '../problem.pddl', keyword1='table', keyaction1='pick', keyword2='red_block',
                      keyword3='yellow_block', keyword4='blue_block', keyword5='None', keyaction2='place')
    string = ComplexTestCases.TEST5.value
    act = Action('../domain.pddl', '../problem.pddl', string, op)
    hehe = act.retrieve_action(3 ,3)
    pepe = act.retrieve_start_state()
    print(f"Action: {hehe}")
    print(f"PEPE: {pepe}")
