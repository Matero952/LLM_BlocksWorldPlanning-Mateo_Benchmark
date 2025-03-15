#Pipeline file to essentially create one track_state function.
import os
from OutputParser import OutputParser
from Action import Action
from ActionOperator import ActionOperator
# from StateTrackerAlgo.Action import NoActionException
from tests.ComplexTestCases import ComplexTestCases
import gymnasium.envs.classic_control as classic_control

class Pipe:
    def __init__(self, domain_file: str, problem_file: str, model_output: str, index):
        assert os.path.exists(domain_file)
        assert os.path.exists(problem_file)
        assert type(model_output) is str, "Model output must be a string"
        self.output_parser = OutputParser('../domain.pddl', '../problem.pddl', keyword1='table', keyaction1='pick', keyword2='red_block', keyword3='yellow_block', keyword4='blue_block', keyword5='None', keyaction2='place')
        self.action_dict = self.output_parser.parse(model_output, 3, 3)
        self.action = Action('../domain.pddl', '../problem.pddl', self.action_dict, index)
        self.action_operator = ActionOperator('../domain.pddl', '../problem.pddl', self.action)
        if self.action.pyperplan_action is not None:
            self.new_state = self.pipeline()
        else:
            self.new_state = self.action.unfiltered_initial_state

    def pipeline(self):
        block_placement, unfiltered_initial_state = self.action.get_pyperplan_initial_state(['clear', 'handempty'])
        cleaned_unfiltered_initial_state = {str(item).strip().lower() for item in unfiltered_initial_state}
        cleaned_action_preconditins = {str(item).strip().lower() for item in self.action_operator.operator.preconditions}
        #TODO Fix pyperplan assertion error stuff
        print(cleaned_action_preconditins <= cleaned_unfiltered_initial_state)
        new_state = ActionOperator.apply_operator(self.action_operator.operator, unfiltered_initial_state)
        return new_state

if __name__ == '__main__':
    test = ComplexTestCases.TEST4.value
    pipe = Pipe('../domain.pddl', '../problem.pddl', test, 0)
    print(pipe.pipeline())



