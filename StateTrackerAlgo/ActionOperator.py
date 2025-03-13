from Action import Action
from OutputParser import OutputParser
#Coming soon.
class BadModelPrediction(Exception):
    def __init__(self, message="Model prediction does not work."):
        super().__init__(message)

class ActionOperator:
    def __init__(self, action: Action, domain_file, problem_file, output_parser: OutputParser, model_output):
        #Inherits from action because we need a few attributes from it.
        #Only thing this class should be handling is the conversation of an action to an operator.
        self.action = Action(domain_file, problem_file, model_output, output_parser)
        self.domain_file = domain_file
        self.problem_file = problem_file
        self.output_parser = OutputParser(domain_file, problem_file, keyword1=None, keyaction1=None)
        self.model_output = model_output
