from ActionOperator import Action, ActionOperator
class StateTracker(ActionOperator):
    def __init__(self, start_state, action_operator: ActionOperator, pick_action: bool, problem_file = None):
        super().__init__(None, None, None, None, problem_file, pick_action)
        self.state_state = start_state
        self.action_operator = action_operator
        self.problem_file = problem_file
