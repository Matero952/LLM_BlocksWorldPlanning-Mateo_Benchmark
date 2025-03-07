import ast
import csv
import regex as re
from pyperplan.task import Operator
from pyperplan.pddl.parser import Parser, Predicate
class Action:
    def __init__(self, csv_index):
        self.csv_index = csv_index
        self.name = 'pick_place'
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
    def write_action_operator(self, row, action, output_path) -> None:
        start_state = ast.literal_eval(row[0])
        end_state = ast.literal_eval(row[1])
        action = ast.literal_eval(action)
        with open(output_path, 'w') as f:
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
            else:
                line = f"pick-up {action['pick']}"
                f.write(line)
            if end_state[action['pick']] != "table":
                #If the object is not going to be placed on the table
                line = f"\nstack {action['pick']} {end_state[action['pick']]}"
                f.write(line)
            else:
                line = f"\nput-down {action['pick']}"
                f.write(line)
        return None
class ActionOperator(Action):
    def __init__(self, csv_index, action: Action):
        super().__init__(csv_index)
        self.action = action




# class ActionOperator():
#     pass


if __name__ == "__main__":
    action = Action(csv_index=10)
    print((action.get_action('ground_truth.csv')))
    action.write_action_operator(action.get_row('ground_truth.csv'), action.get_action('ground_truth.csv'), 'hehe.pddl.soln')

