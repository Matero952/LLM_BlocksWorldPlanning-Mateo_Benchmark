import ast
import csv
import sys
import regex as re
from pyperplan.pddl.parser import Parser
from pyperplan.task import Operator

class Action:
    def __init__(self, problem_file, action, output_path):
        self.problem_file = problem_file
        self.action = self.__parse_action__(action) if type(action) is str else action
        self.output_path = output_path
        self.names = None
        self.pick_action = None
        self.place_action = None
        #Initializes later
        self.start_state, self.end_state = self.__retrieve_problem__()

    def __parse_action__(self, action):
        action_dict = {}
        blocks = re.findall(r"\b\w*_block\b", action)
        assert len(blocks) >= 2
        action_dict['pick'] = blocks[0]
        action_dict['place'] = blocks[1]
        return action_dict

    def __write_action_operator__(self):
        start_state = self.start_state
        end_state = self.end_state

        with open(self.output_path, 'w') as f:
            #Check 'None'
            if self.action['pick'] == "None":
                line0 = f""
                line1 = f"\n"
                f.write(line0)
                f.write(line1)
                return None
            #First pick/unstack
            if start_state[self.action['pick']] != "table":
                #If the object is not on the table
                line = f"(unstack {self.action['pick']} {start_state[self.action['pick']]})"
                f.write(line)
                self.pick_action = 'unstack'
            else:
                line = f"(pick-up {self.action['pick']})"
                f.write(line)
                self.pick_action = 'pick-up'
            if end_state[self.action['pick']] != "table":
                #If the object is not going to be placed on the table
                line = f"\n(stack {self.action['pick']} {end_state[self.action['pick']]})"
                f.write(line)
                self.place_action = 'stack'
            else:
                line = f"\n(put-down {self.action['pick']})"
                f.write(line)
                self.place_action = 'put-down'
        return None
        #Returns nothing
    def get_operator_bindings(self) -> dict:
        op_bindings = {'?x' : self.action['pick'], '?y' : self.action['place']}
        return op_bindings

    def __retrieve_problem__(self):
        initial_placement_map = {}
        final_placement_map = {}
        parser = Parser('domain.pddl', 'problem.pddl')
        domain = parser.parse_domain(True)
        problem = parser.parse_problem(domain, True)
        self.names = problem.name
        initial_states = problem.initial_state[:3]
        final_states = problem.goal[:3]
        #Only first three are important, which problem.goal is already but just in case
        for state in initial_states:
            block = re.findall(r"\b\w*_block\w*\b", str(state))
            if len(block) < 2:
                initial_placement_map[block[0]] = 'table'
            else:
                initial_placement_map[block[0]] = block[1]
        for state in final_states:
            block = re.findall(r"\b\w*_block\w*\b", str(state))
            if len(block) < 2:
                final_placement_map[block[0]] = 'table'
            else:
                final_placement_map[block[0]] = block[1]
        return initial_placement_map, final_placement_map

class ActionOperator(Action):
    def __init__(self, output_path, action: Action, domain_file, problem_file, pick_action: bool):
        super().__init__(problem_file=problem_file, action=action, output_path=output_path)
        self.action = action
        self.domain_file = domain_file
        self.problem_file = problem_file
        self.parser = Parser(domain_file, problem_file)
        self.action_preconditions, self.add_effects, self.del_effects = self.substitute_params(pick_action)
        self.action_operator = Operator(name=self.action.names, preconditions=self.action_preconditions, add_effects=self.add_effects, del_effects=self.del_effects)
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
            continue
        updated_preconditions = updated_preconditions & self.action_preconditions
        return updated_preconditions
        #Only return preconditions shared in the lists.

    #TODO REWRITE THIS FUNCTION
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
        #'Just in case' pyperplan compatibility check.
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
    example_action = "pick: red_block place: yellow_block"
    ba = Action('problem.pddl', example_action, 'hehe.pddl.soln')
    ao = ActionOperator('hehe.pddl', ba, 'domain.pddl', 'problem.pddl', pick_action=True)
    print(ao.get_action_preconditions())
    print(ba.__retrieve_problem__())
    ba.__parse_action__(example_action)
    ba.__write_action_operator__()
    print(ba.get_operator_bindings())



# class StateTracker(ActionOperator):
#     def __init__(self, action: Action, action_operator: ActionOperator, problem_file: str, pick_action: bool, domain_file):
#         super().__init__(csv_index=action_operator.csv_index, action=action, problem_file=problem_file, pick_action=pick_action, domain_file=domain_file, output_path=None)
#         self.action = action
#         self.action_operator = action_operator
#         self.problem_file = problem_file
#         self.pick_action = pick_action
#         self.domain_file = domain_file
#         self.action_preconditions, self.add_effects, self.del_effects = self.substitute_params(pick_action)
#     def __apply_operator__(self):
#         state_preconditions = self.get_state_preconditions()
#         available = self.fulfilled_preconditions(pick_action=self.pick_action)
#         if not available:
#             print(f"Operator not applicable: {self.action_operator.action_operator}")
#             print(f"State_preconditions: {state_preconditions}")
#             return state_preconditions
#         else:
#             new_state = state_preconditions.copy()
#             new_state.difference_update(self.del_effects)
#             new_state.update(self.add_effects)
#             #Returns new state
#             return new_state
#     #TODO Also make sure to turn csv index into an action parameter for more widespread parsing.
#
# if __name__ == "__main__":
#     action = Action(csv_index=13, output_path='hehe.pddl.soln')
#     print((action.get_action('ground_truth.csv')))
#     action.write_action_operator(action.get_row('ground_truth.csv'), action.get_action('ground_truth.csv'))
#     actionop = ActionOperator(13, 'hehe.pddl', action, 'domain.pddl', 'problem.pddl', True)
#     st= StateTracker(action, actionop, problem_file='problem.pddl', pick_action=True, domain_file='domain.pddl')
#     print(st.__apply_operator__())
#     print(f"New state: {st.__get_new_state__()}")