from Action import Action
from OutputParser import OutputParser
from pyperplan.task import Operator
from tests.ComplexTestCases import ComplexTestCases

#Coming soon.
class BadModelPrediction(Exception):
    def __init__(self, message="Model prediction does not work."):
        super().__init__(message)

class ActionOperator:
    def __init__(self, domain_file, problem_file, action: Action):
        #Inherits from action because we need a few attributes from it.
        #Only thing this class should be handling is the conversation of an action to an operator.
        self.action = action
        self.domain_file = domain_file
        self.problem_file = problem_file
        self.operator = self.write_operator()

    def write_operator(self):
        name = self.action.pyperplan_action
        preconditions = self.action.action_preconditions
        add_effects = self.action.add_effects
        del_effects = self.action.del_effects
        action_operator = Operator(name, preconditions, add_effects, del_effects)
        return action_operator

    @staticmethod
    def apply_operator(action_operator: Operator, state: frozenset):
        print(f"Applying {action_operator}")
        print(f"state: {state}")
        new_state = action_operator.apply(state)
        print(f"State prime: {new_state}")
        return new_state

    @staticmethod
    def normalize_predicates(predicates):
        #Please note that this function is like only used in my custom applicable function bc pyperplan was being silly.
        return None



    @staticmethod
    def custom_applicable(action_predicates, state_predicates):
        return None

if __name__ == "__main__":
    pass

