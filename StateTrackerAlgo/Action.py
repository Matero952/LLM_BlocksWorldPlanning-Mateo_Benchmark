from OutputParser import OutputParser
from tests.ComplexTestCases import ComplexTestCases
from pyperplan.pddl.parser import Parser
from pyperplan.pddl.pddl import Predicate
from pyperplan.pddl.pddl import Type
import os
import ast

class Action:
    def __init__(self, domain, problem, action_dict: list, index):
        self.domain = domain
        self.problem = problem
        self.object_mapping = {}
        counter = 0
        for i in action_dict:
            for key, value in i.items():
                if counter % 2 == 0:
                    self.object_mapping['?x'] = value.strip().lower()
                else:
                    self.object_mapping['?y'] = value.strip().lower()
                counter += 1
        self.action = action_dict[index]
        self.pddl_parser = Parser(domain, problem)
        self.pyperplan_action = self.write_sol_file('../hehe.pddl.soln', ['clear', 'handempty'])
        #Retrieves the action and writes the solution file at same time
        self.action_preconditions, self.add_effects, self.del_effects = self.get_param_action_attrs()

        self.block_placement, self.unfiltered_initial_state = self.get_pyperplan_initial_state(['clear', 'handempty'])

    def get_pyperplan_initial_state(self, ignore_list):
        #Basically just gets the start state
        domain_parsed = self.pddl_parser.parse_domain(True)
        problem_parsed = self.pddl_parser.parse_problem(domain_parsed, True)
        unfiltered_initial_state = problem_parsed.initial_state
        block_placement = self.parse_initial_state(unfiltered_initial_state, ignore_list)
        unfiltered_initial_state = frozenset([predicate for predicate in unfiltered_initial_state])
        return block_placement, unfiltered_initial_state

    def write_sol_file(self, output_path: str,ignore_list) -> str or bool:
        assert os.path.exists(output_path)
        start_state, _ = self.get_pyperplan_initial_state(ignore_list)
        with open(output_path, "w") as f:
            for key, value in self.action.items():
                if key == 'pick':
                    if value != 'None':
                        if start_state[value] == 'table':
                            line0 = f"(pick-up {value})"
                            # Pick up if it is mapped to the table
                            action = 'pick-up'
                            f.write(line0)
                        else:
                            line0 = f"(unstack {value} {start_state[value]})"
                            action = 'unstack'
                            f.write(line0)
                    else:
                        return None
                elif key == 'place':
                    if value != 'None':
                        if value == 'table':
                            line0 = f"(put-down {value})"
                            action = 'put-down'
                            f.write(line0)
                        else:
                            line0 = f"(stack {value} {start_state[value]})"
                            action = 'stack'
                            f.write(line0)
                    else:
                        return None
                else:
                    raise ValueError('Key is not an expected value.')
        return action

    def get_param_action_attrs(self):
        domain = self.pddl_parser.parse_domain(True)
        print(f"pyperplan aciton: {self.pyperplan_action}")
        for action_name, action in domain.actions.items():
            if action_name == self.pyperplan_action:
                print(f"matching action: {action_name}")
                precondition = action.precondition
                add_effect = action.effect.addlist
                del_effect = action.effect.dellist
                return frozenset(self.deparam_action_attr(precondition, self.object_mapping)),frozenset(self.deparam_action_attr(add_effect, self.object_mapping)), frozenset(self.deparam_action_attr(del_effect, self.object_mapping))
            elif self.pyperplan_action is None:
                return frozenset(), frozenset(), frozenset()
    #Helper functions
    @staticmethod
    def parse_initial_state(initial_state: list, ignore: list):
        block_placement = {}
        for placement in initial_state:
            skip = Action.filter_ignore(placement, ignore)
            if skip:
                continue
            block_placement[tuple(placement.signature)] = placement.name
        block_placement = Action.get_start_state(block_placement)
        block_placement = Action.extract_object(block_placement, ['red_block', 'blue_block', 'yellow_block'])
        return block_placement

    @staticmethod
    def filter_ignore(placement: Predicate, ignore_list: list):
        #If the placement type needs to be ignored, return true.
        if placement.name in ignore_list:
            return True
        return False

    @staticmethod
    def get_start_state(block_placement: dict):
        updated_block_placement = {}
        for key, value in block_placement.items():
            assert value is not None
            if value == 'ontable':
                updated_block_placement[key] = 'table'
            elif value == 'on':
                top_block, bottom_block = key
                updated_block_placement[top_block] = bottom_block
            else:
                return None
        return updated_block_placement

    @staticmethod
    def extract_object(block_placement, objects):
        updated_block_placement = {}
        for key, value in block_placement.items():
            key = [i for i in key if i is not None][0]
            if type(key) is tuple:
                key, _ = key
            else:
                pass
            if type(value) is tuple:
                value, _ = value
            else:
                pass
            for object in objects:
                if key in object:
                    updated_block_placement[object] = value
        return updated_block_placement

    @staticmethod
    def deparam_action_attr(action_att_with_param, object_attr_dict):
        new_list = []
        #makeshift object type class solution please update and make dynamic
        for key, value in object_attr_dict.items():
            for predicate in action_att_with_param:
                if 0 < len(predicate.signature):
                    # variable, var_type = predicate.signature[0]
                    variable, original_type = predicate.signature[0]
                    if key in variable:
                        predicate.signature[0] = value.strip().lower(), original_type[0] if type(original_type) is list else original_type
                        new_list.append(predicate)
                else:
                    new_list.append(predicate)
        return frozenset(new_list)



if __name__ == '__main__':
    model_output = ComplexTestCases.TEST3.value
    op = OutputParser('../domain.pddl', '../problem.pddl', keyword1='table', keyaction1='pick', keyword2='red_block',
                      keyword3='yellow_block', keyword4='blue_block', keyword5='None', keyaction2='place')
    action_dict = op.parse(model_output, 3, 3)
    action = Action('../domain.pddl', '../problem.pddl', action_dict, 0)
    print(action.get_param_action_attrs())

