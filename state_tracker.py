import argparse
import ast
import subprocess
import csv
from typing import FrozenSet

import regex as re
import pandas as pd
from pyperplan.task import Operator
from pyperplan.pddl.parser import Parser

class OperatorGetter:
    def __init__(self):
        pass
    def format_action(self, state, action, output_file, domain_file=None, problem_file=None) -> Operator:
        '''Function to take in an action and convert to operator
        because editing pyperplan library was too difficult.'''
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
        #TODO Fix this monstrosity
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
        preconditions, add_effects, del_effects = self.parse_pddl(domain_file, problem_file, output_file)
        operator = Operator(name=formed_action, preconditions=preconditions, add_effects=add_effects, del_effects=del_effects)
        print(f"Operator: {operator}")
        return operator
    def parse_pddl(self, domain_file, prob_file, formatted_action_file) -> tuple[frozenset, frozenset, frozenset] or None:
        '''Function to parse formatted_action_file pddl and retrieve important
        stuff for Operator object.'''
        assert (type(domain_file) == str and type(prob_file) == str and
                type(formatted_action_file) == str)
        #Files must be strings
        with open(formatted_action_file, 'r') as f:
            first_line = f.readline().strip()
            found_action = re.search(r"\(\s*(\S+)", first_line).group(1)
            print(f"Action1: {found_action}")
            #Extracting action from format_action
            if not found_action:
                raise ValueError("Action isnt valid.")
            #Action must be valid yk
        parser = Parser(domain_file, prob_file)
        domain_parsed = parser.parse_domain(read_from_file=True)
        problem_parsed = parser.parse_problem(dom=domain_parsed, read_from_file=True)
        #Self-explanatory?!
        for action_name, action in domain_parsed.actions.items():
            if found_action != action_name:
                continue
                #Skips to next
            else:
                add_effect = frozenset(action.effect.addlist)
                del_effect = frozenset(action.effect.dellist)
                precondition = frozenset(action.precondition)
                #Pyperplan expecting hashable, immutable type, so I just use a frozenset.
                return precondition, add_effect, del_effect
                #Return values are used for making Operator object.
class StateTracker(OperatorGetter):
    def __init__(self):
        super().__init__()
    def apply_operator(self, state, operator) -> str:
        #TODO Read documentation on this.
        return 'None'




if __name__=='__main__':
    example_action = "{""pick"": ""yellow_block"", ""place"": ""red_block""}"
    example_state = "{""red_block"": ""table"", ""blue_block"": ""table"", ""yellow_block"": ""table""}","{""red_block"": ""table"", ""blue_block"": ""table"", ""yellow_block"": ""table""}","{""pick"": ""None"", ""place"": ""None""}","""0"""
    op = OperatorGetter()
    op.format_action(domain_file='domain.pddl', problem_file='problem.pddl', state=example_state, action=example_action, output_file='hehe.pddl.soln')