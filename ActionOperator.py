import ast
import csv
from pyperplan.pddl.parser import Parser
from pyperplan.task import Operator

class Action:
    def __init__(self, csv_index, output_path):
        self.csv_index = csv_index
        self.pick_action = None
        self.place_action = None
        self.names = (self.pick_action, self.place_action)
        self.output_path = output_path
        self.action = None

    def get_action(self, csv_path):
        with open(csv_path, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)
            return rows[self.csv_index][2]

    def get_row(self, csv_path):
        with open(csv_path, 'r') as f:
            reader = csv.reader(f)
            rows = list(reader)
            return rows[self.csv_index]

    #Helper function.
    def write_action_operator(self, row, action):
        start_state = ast.literal_eval(row[0])
        end_state = ast.literal_eval(row[1])
        action = ast.literal_eval(action)
        self.action = action
        #Overwrite action
        with open(self.output_path, 'w') as f:
            #Check 'None'
            if action['pick'] == "None":
                line0 = f""
                line1 = f"\n"
                f.write(line0)
                f.write(line1)
                return None
            #First pick/unstack
            if start_state[action['pick']] != "table":
                #If the object is not on the table
                line = f"unstack {action['pick']} {start_state[action['pick']]}"
                f.write(line)
                self.pick_action = 'unstack'
            else:
                line = f"pick-up {action['pick']}"
                f.write(line)
                self.pick_action = 'pick-up'
            if end_state[action['pick']] != "table":
                #If the object is not going to be placed on the table
                line = f"\nstack {action['pick']} {end_state[action['pick']]}"
                f.write(line)
                self.place_action = 'stack'
            else:
                line = f"\nput-down {action['pick']}"
                f.write(line)
                self.place_action = 'put-down'
        return None
        #Returns nothing


    def get_operator_bindings(self) -> dict:
        op_bindings = {'?x' : self.action.action['pick'], '?y' : self.action.action['place']}
        return op_bindings

class ActionOperator(Action):
    def __init__(self, csv_index, output_path, action: Action, domain_file, problem_file, pick_action: bool):
        super().__init__(csv_index, output_path)
        self.action = action
        self.domain_file = domain_file
        self.problem_file = problem_file
        self.parser = Parser(domain_file, problem_file)
        self.action_preconditions, self.add_effects, self.del_effects = self.substitute_params(pick_action)
        self.action_operator = Operator(self.action.names, self.action_preconditions, self.add_effects, self.del_effects)

    def get_action_preconditions(self, pick_action=False):
        #Parsing parameterized action preconditions
        domain_parsed = self.parser.parse_domain(read_from_file=True)
        for action_name, dom_action in domain_parsed.actions.items():
            if (self.action.pick_action != action_name) if pick_action else (self.action.place_action != action_name):
                continue
                # Skips to next
            else:
                add_effect = frozenset(dom_action.effect.addlist)
                del_effect = frozenset(dom_action.effect.dellist)
                precondition = frozenset(dom_action.precondition)
                # Pyperplan expecting hashable, immutable type, so I just use a frozenset.
                return precondition, add_effect, del_effect
        return frozenset(), frozenset(), frozenset()
        #Happens if pick action is None. Preconditions are essentially met.

    def get_state_preconditions(self):
        #Parsing non-parameterized state preconditions
        domain_parsed = self.parser.parse_domain(read_from_file=True)
        problem_parsed = self.parser.parse_problem(domain_parsed, read_from_file=True)
        #Parses domain for problem
        updated_preconditions = set()
        preconditions = set(problem_parsed.initial_state)
        for precondition in preconditions:
            updated_preconditions.add(str(precondition))
        return updated_preconditions

    def substitute_params(self, pick_action: bool):
        #TODO Fix this function please ):
        action_preconditions, add_effects, del_effects = self.get_action_preconditions(pick_action)
        action_preconditions = set(action_preconditions)
        add_effects = set(add_effects)
        del_effects = set(del_effects)
        #Overwrite action_preconditions from frozenset -> set
        updated_preconditions = set()
        updated_add_effects = set()
        updated_del_effects = set()
        for precondition in action_preconditions:
            precondition = str(precondition).replace('?x', self.get_operator_bindings()['?x'])
            precondition = str(precondition).replace('?y', self.get_operator_bindings()['?y'])
            precondition = str(precondition).replace('[object]', 'object')
            updated_preconditions.add(ast.literal_eval(precondition)) if type(precondition) is not str else updated_preconditions.add(precondition)
            #Adding fixed element
        print(f"new action_preconditions: {action_preconditions}")
        for add_effect in add_effects:
            add_effect = str(add_effect).replace('?x', self.get_operator_bindings()['?x'])
            add_effect = str(add_effect).replace('?y', self.get_operator_bindings()['?y'])
            add_effect = str(add_effect).replace('[object]', 'object')
            updated_add_effects.add(ast.literal_eval(add_effect)) if type(add_effect) is not str else updated_add_effects.add(add_effect)
        for del_effect in del_effects:
            del_effect = str(del_effect).replace('?x', self.get_operator_bindings()['?x'])
            del_effect = str(del_effect).replace('?y', self.get_operator_bindings()['?y'])
            del_effect = str(del_effect).replace('[object]', 'object')
            updated_del_effects.add(ast.literal_eval(del_effect)) if type(del_effect) is not str else updated_del_effects.add(del_effect)
        return updated_preconditions, updated_add_effects, updated_del_effects

    def fulfilled_preconditions(self, pick_action: bool) -> bool:
        #Checks if our state fulfills and necessary action preconditions
        state_preconditions = self.get_state_preconditions()
        action_preconditions, _, _ = self.substitute_params(pick_action)
        print(f"state_preconditions: {state_preconditions}")
        print(f"action_preconditions: {action_preconditions}")
        for precondition in action_preconditions:
            if precondition not in state_preconditions:
                print(f"Missing precondition: {precondition}")
                #Necessary preconditions not met
                return False
            else:
                continue
        #Necessary preconditions met
        return True

if __name__ == "__main__":
    action = Action(csv_index=5, output_path='hehe.pddl.soln')
    print((action.get_action('ground_truth.csv')))
    action.write_action_operator(action.get_row('ground_truth.csv'), action.get_action('ground_truth.csv'))
    actionop = ActionOperator(5, 'hehe.pddl', action, 'domain.pddl', 'problem.pddl', True)
    print(actionop.fulfilled_preconditions(True))