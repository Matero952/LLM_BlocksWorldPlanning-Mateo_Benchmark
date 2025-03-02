import argparse
import ast
import subprocess
import csv
import regex as re
from pyperplan.grounding import ground
from pyperplan.task import Task, Operator
from pyperplan.pddl import parser
import pyperplan

class StateTracker:
    def __init__(self, domain_file, problem_file, ground_truth_file):
        self.domain_file = domain_file
        self.problem_file = problem_file
        self.ground_truth_file = ground_truth_file
    def is_available(self, index, action) -> bool:
        with open(self.ground_truth_file, "r") as f:
            entry = f[index]
            print(f"Entry: {entry}")

    def is_available(self, line, action, check = False) -> bool:
        '''This function runs a bunch of tests to make sure that
        the model's prediction is actually possible within the world'''
        cleared_blocks = []
        start_state = line[0]
        print(f"start_state: {start_state}")
        print(f"Start state: {start_state}, type: {type(start_state)}")
        fixed_action = ast.literal_eval(re.sub(r'"', '', action))
        print(f"Fixed action: {fixed_action}, type: {type(fixed_action)}")
        if fixed_action['pick'] != fixed_action['place'] or fixed_action['place'] == 'None' and fixed_action['pick'] == 'None':
            check = True





if __name__=="__main__":
    statetracker = StateTracker("domain.pddl", "problem.pddl", "ground_truth.csv")
    example_line = "{""red_block"": ""table"", ""blue_block"": ""table"", ""yellow_block"": ""table""}","{""red_block"": ""table"", ""blue_block"": ""table"", ""yellow_block"": ""table""}","{""pick"": ""None"", ""place"": ""None""}","""0"""
    example_action = "{'pick': 'yellow_block', 'place': 'yellow_block'}"
    statetracker.is_available(example_line, example_action)









