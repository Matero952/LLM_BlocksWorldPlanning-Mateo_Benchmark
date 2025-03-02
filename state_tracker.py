import argparse
import ast
import subprocess
import csv
import regex as re
import pandas as pd
import fast_downward as fd
import subprocess
#TODO Put correct path into fd_command
#TODO Make this adapatable for path planning and action availability.
class FDPipeline:
    def __init__(self, domain_file, problem_file, ground_truth_file):
        self.domain_file = domain_file
        self.problem_file = problem_file
        self.ground_truth_file = ground_truth_file
    def pipe(self, start_state, end_state, action):
        if start_state is None or end_state is None:
            raise ValueError("start_state and end_state are required")
        else:
            print(f"start_state: {start_state}, end_state: {end_state}, action: {action}") if action is not None else None
        fd_command = [
            "Replace this with correct path",
            self.domain_file,
            self.problem_file,
            "--search",
            "eager_greedy(ff(), "
            "reopen_closed=false),"
            "--helpful_transitions=false"
        ]
        result = subprocess.run(fd_command, capture_output=True, text=True)
        #Do iteration stuff here to find all possible next moves. Then,
        #we can append these moves to the


class StateTracker(FDPipeline):
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
    statetracker = StateTracker("domain.pddl", "problem.pddl", "ground_truth.csv")
    example_line = "{""red_block"": ""table"", ""blue_block"": ""table"", ""yellow_block"": ""table""}","{""red_block"": ""table"", ""blue_block"": ""table"", ""yellow_block"": ""table""}","{""pick"": ""None"", ""place"": ""None""}","""0"""
    example_action = "{'pick': 'yellow_block', 'place': 'yellow_block'}"
    statetracker.available_action(2, example_action)









