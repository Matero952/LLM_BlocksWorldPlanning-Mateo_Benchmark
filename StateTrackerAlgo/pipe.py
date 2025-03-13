#Pipeline file to essentially create one track_state function.
import os
from OutputParser import OutputParser
from Action import Action
from ActionOperator import ActionOperator
class Pipe:
    def __init__(self, domain_file: str, problem_file: str, model_output: str, index):
        assert os.path.exists(domain_file)
        assert os.path.exists(problem_file)
        assert type(model_output) is str, "Model output must be a string"
        self.output_parser = OutputParser('../domain.pddl', '../problem.pddl', keyword1='table', keyaction1='pick', keyword2='red_block', keyword3='yellow_block', keyword4='blue_block', keyword5='None', keyaction2='place')
        self.action_dict = self.output_parser.parse(model_output, 3, 3)
        self.action = Action('../domain.pddl', '../problem.pddl', self.action_dict, index)
        self.action_operator = ActionOperator('../domain.pddl', '../problem.pddl', self.action)

    def pipeline(self):
        block_placement, unfiltered_initial_state = self.action.parse_initial_state()
        ActionOperator.apply_operator(self.action_operator, )



