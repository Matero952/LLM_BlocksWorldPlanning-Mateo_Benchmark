import argparse
import ast
import subprocess
import csv
import regex as re
import pandas as pd

#TODO Make this adapatable for path planning and action availability.
class OperatorGetter:
    def __init__(self):
        pass
    def action_to_operator(self, state, action, output_file) -> None:
        '''Function to take in an action and convert to operator
        because editing pyperplan library was too difficult.'''
        #Example action: "{""pick"": ""None"", ""place"": ""None""}"
        #Example state: "{""red_block"": ""table"", ""blue_block"": ""table"", ""yellow_block"": ""table""}"
        #State filtering first
        formed_state = state[0]
        formed_state = (re.sub(r'(\w+):\s*(\w+)', r"'\1': '\2'", formed_state))
        formed_state = ast.literal_eval(formed_state)
        assert type(formed_state) == dict, "Formed_state is not a dict"
        print(f"Formed_state: {formed_state}, Type: {type(formed_state)}")
        unstackable = []
        pick_upable = []
        for key, value in formed_state.items():
            if value == 'table':
                pick_upable.append(key)
                assert key not in unstackable
            else:
                unstackable.append(key)
                assert key not in pick_upable
        assert type(action) == str, 'Action must be a string(1)'
        formed_action = re.sub(r'(\w+): (\w+)', r"'\1': '\2'", action)
        if not formed_action:
            raise TypeError('Whoopsies')
        assert type(formed_action) == str, 'Action must be a string(2)'
        formed_action = ast.literal_eval(formed_action)
        assert type(formed_action) == dict, 'Action must be a dict(1)'
        assert formed_action['pick'] != formed_action['place']
        if formed_action['pick'] in unstackable:
            print(f"{formed_action['pick']} is unstackable")
        elif formed_action['pick'] in pick_upable:
            print(f"{formed_action['pick']} is pick_upable")
        elif formed_action['place'] in pick_upable:
            print(f"{formed_action['place']} is pick_upable")
        else:
            raise ValueError(f"Action must be unstackable or pick_upable")
        print(f"Unstackable: {unstackable}, pick_upable: {pick_upable}")
        with open(output_file, 'w') as f:
            if formed_action['pick'] in pick_upable:
                f.write(f"(pick-up {formed_action['pick']})")
            else:
                f.write(f"\n(unstack {formed_action['pick']})" + ')')
            if formed_action['place'] == 'table':
                f.write(f"\n(put-down {formed_action['pick']}" +')')
            else:
                f.write(f"\n(stack {formed_action['pick']} {formed_action['place']}" + ')')
        return None

if __name__=='__main__':
    example_action = "{""pick"": ""yellow_block"", ""place"": ""table""}"
    example_state = "{""red_block"": ""table"", ""blue_block"": ""table"", ""yellow_block"": ""table""}","{""red_block"": ""table"", ""blue_block"": ""table"", ""yellow_block"": ""table""}","{""pick"": ""None"", ""place"": ""None""}","""0"""
    op = OperatorGetter()
    op.action_to_operator(example_state ,example_action, 'hehe.pddl.soln')
















# class pyplanpipeline:
#     def __init__(self, ground_truth_file):
#         self.ground_truth_file = ground_truth_file
#     def pipe(self, domain_file, problem_file):
#         pyplan_command = ["pyperplan", "--heuristic", "blind", "--search", "bfs", domain_file, problem_file]
#         #'astar' is replaced by 'bfs' to search all valid paths
#         #'hff' is also replaced 'blind' to treat all states equally
#         result = (subprocess.run(pyplan_command, capture_output=True, text=True)).stdout
#         print(f"result: {result}")
#         filtered_result = self.retrieve_from_log(result, r"^.*?Possible moves:(.*)$", target_key="Possible moves")
#         print(f"Filtered_result: {filtered_result}")
#         return filtered_result
#     def retrieve_from_log(self, result, regex, target_key):
#         result = result.splitlines()
#         print(f"Result: {result}")
#         found = False
#         for indice in result:
#             if target_key in indice:
#                 target = (re.search(regex, indice, re.IGNORECASE)).group(1)
#                 found = True
#                 return target
#             else:
#                 pass
#         if not found:
#             raise ValueError(f"Failed to find {target_key}")
#
# class StateTracker(pyplanpipeline):
#     def __init__(self, domain_file, ground_truth_file):
#         super().__init__(ground_truth_file)
#         self.domain_file = domain_file
#         self.ground_truth_file = ground_truth_file
#     def available_action(self, index, action):
#         available_actions = []
#         with open(self.ground_truth_file) as ground_truth_file:
#             data = pd.read_csv(ground_truth_file)
#             data = data.to_dict('records')
#             entry = data[index]
#             action = ast.literal_eval(action)
#             print(f"data: {data}, "
#                   f"entry: {entry}, "
#                   f"action: {action}")
# if __name__=="__main__":
#     # statetracker = StateTracker("domain.pddl", "problem.pddl", "ground_truth.csv")
#     # example_line = "{""red_block"": ""table"", ""blue_block"": ""table"", ""yellow_block"": ""table""}","{""red_block"": ""table"", ""blue_block"": ""table"", ""yellow_block"": ""table""}","{""pick"": ""None"", ""place"": ""None""}","""0"""
#     # example_action = "{'pick': 'yellow_block', 'place': 'yellow_block'}"
#     # statetracker.available_action(2, example_action)
#     pp = pyplanpipeline(ground_truth_file='ground_truth.csv')
#     result = pp.pipe("./domain.pddl", "./problem.pddl")
#     print(f"type: {type(result)}")
#     # filtered_result = pp.retrieve_from_log(result, r"Possible moves:\s*(\[[^\]]*\])", target_key="Possible moves")
#     # print(f"filtered_result: {filtered_result}")









