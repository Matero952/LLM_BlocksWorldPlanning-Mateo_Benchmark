import ast
import csv
import regex as re
from pyperplan.task import Operator
from pyperplan.pddl.parser import Parser, Predicate
class Action:
    def __init__(self, csv_index, output_path):
        self.csv_index = csv_index
        self.pick_action = None
        self.place_action = None
        self.names = tuple[self.pick_action, self.place_action]
        self.output_path = output_path
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
    def write_action_operator(self, row, action) -> None:
        start_state = ast.literal_eval(row[0])
        end_state = ast.literal_eval(row[1])
        action = ast.literal_eval(action)
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
class ActionOperator(Action):
    def __init__(self, csv_index, output_path, action: Action, domain_file, problem_file):
        super().__init__(csv_index, output_path)
        self.action = action
        self.domain_file = domain_file
        self.problem_file = problem_file
        self.parser = Parser(domain_file, problem_file)
    def get_action_preconditions(self):
        domain_parsed = self.parser.parse_domain(read_from_file=True)
        for action_name, dom_action in domain_parsed.actions.items():
            if action.pick_action != action_name:
                continue
                # Skips to next
            else:
                add_effect = frozenset(dom_action.effect.addlist)
                del_effect = frozenset(dom_action.effect.dellist)
                precondition = frozenset(dom_action.precondition)
                # Pyperplan expecting hashable, immutable type, so I just use a frozenset.
                return precondition, add_effect, del_effect











if __name__ == "__main__":
    action = Action(csv_index=10)
    print((action.get_action('ground_truth.csv')))
    action.write_action_operator(action.get_row('ground_truth.csv'), action.get_action('ground_truth.csv'), 'hehe.pddl.soln')

