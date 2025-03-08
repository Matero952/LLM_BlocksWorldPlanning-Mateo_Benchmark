from ActionOperator import Action, ActionOperator
from pyperplan.task import Operator
class StateTracker(ActionOperator):
    def __init__(self, start_state, action_operator: ActionOperator, pick_action: bool, problem_file = None):
        super().__init__(None, None, Action, None, problem_file, pick_action)
        #Start state needs to be the set of state preconditions.
        self.start_state = start_state
        self.action_operator = action_operator
        self.problem_file = problem_file
    def apply_operator(self):
        available = self.action_operator.action_operator.applicable(self.start_state)
        print(available) if available else print("Not available")
if __name__=='__main__':
    example_action = Action(2, 'hehe.pddl.soln')
    example_ao = ActionOperator(2, 'hehe.pddl.soln', example_action, 'domain.pddl', 'problem.pddl', True)
    start_state = ActionOperator.get_state_preconditions(example_ao)
    st = StateTracker(start_state, example_ao, True)
    st.apply_operator()


