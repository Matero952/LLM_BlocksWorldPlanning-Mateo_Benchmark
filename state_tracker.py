import argparse
import ast
import subprocess
import csv
import regex as re
import pandas as pd
import subprocess
#TODO Make this adapatable for path planning and action availability.
class pyplanpipeline:
    def __init__(self, ground_truth_file):
        self.ground_truth_file = ground_truth_file
    def pipe(self, domain_file, problem_file):
        pyplan_command = ["pyperplan", "--heuristic", "blind", "--search", "bfs", domain_file, problem_file]
        #'astar' is replaced by 'bfs' to search all valid paths
        #'hff' is also replaced 'blind' to treat all states equally
        result = (subprocess.run(pyplan_command, capture_output=True, text=True)).stdout
        filtered_result = self.retrieve_from_log(result, r"Possible moves:\s*(\[[^\]]*\])", target_key="Possible moves")
        print(f"Filtered result: {filtered_result}")
        return filtered_result
    def retrieve_from_log(self, result, regex, target_key):
        try:
            result = result.stdout.splitlines()
        except AttributeError:
            result = result.splitlines()
            print(f"Result splitlines")
        found = False
        for indice in result:
            if target_key in indice:
                target = (re.search(regex, indice, re.IGNORECASE)).group(1)
                found = True
                return target
            else:
                pass
        if not found:
            raise ValueError(f"Failed to find {target_key}")

class StateTracker(pyplanpipeline):
    def __init__(self, domain_file, ground_truth_file):
        super().__init__(domain_file, ground_truth_file)
        self.domain_file = domain_file
        self.ground_truth_file = ground_truth_file
    def available_action(self, index, action):
        available_actions = []
        with open(self.ground_truth_file) as ground_truth_file:
            data = pd.read_csv(ground_truth_file)
            data = data.to_dict('records')
            entry = data[index]
            action = ast.literal_eval(action)
            print(f"data: {data}, "
                  f"entry: {entry}, "
                  f"action: {action}")
if __name__=="__main__":
    # statetracker = StateTracker("domain.pddl", "problem.pddl", "ground_truth.csv")
    # example_line = "{""red_block"": ""table"", ""blue_block"": ""table"", ""yellow_block"": ""table""}","{""red_block"": ""table"", ""blue_block"": ""table"", ""yellow_block"": ""table""}","{""pick"": ""None"", ""place"": ""None""}","""0"""
    # example_action = "{'pick': 'yellow_block', 'place': 'yellow_block'}"
    # statetracker.available_action(2, example_action)
    pp = pyplanpipeline(ground_truth_file='ground_truth.csv')
    result = pp.pipe("./domain.pddl", "./problem.pddl")
    print(f"type: {type(result)}")
    # filtered_result = pp.retrieve_from_log(result, r"Possible moves:\s*(\[[^\]]*\])", target_key="Possible moves")
    # print(f"filtered_result: {filtered_result}")









