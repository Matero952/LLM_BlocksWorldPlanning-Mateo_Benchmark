import ast
import regex as re
from pyperplan.pddl.parser import Parser
from pyperplan.task import Operator

class BadModelPrediction(Exception):
    def __init__(self, message="Model prediction does not work."):
        super().__init__(message)

class Action:
    def __init__(self, problem_file, input_action, output_path):
        self.problem_file = problem_file
        self.action = self.__parse_action__(input_action) if type(input_action) is str else input_action
        self.output_path = output_path
        _, _, self.name = self.__retrieve_problem__()
        self.start_state, self.end_state, _ = self.__retrieve_problem__()
        self.pick_action, self.place_action = self.__write_action_operator__()
        self.operator_binds = self.get_operator_bindings()

    def __parse_action__(self, action):
        action_dict = {}
        blocks = re.findall(r"\b\w*_block\b|\btable\b", action)
        print(blocks)
        action_dict['pick'] = blocks[0]
        action_dict['place'] = blocks[1]
        if action_dict['pick'] == action_dict['place'] and action_dict['pick'] != 'None':
            raise BadModelPrediction()
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
                pick_action = 'None'
                place_action = 'None'
                return pick_action, place_action
            #First pick/unstack
            print(f"Start state: {start_state}")
            if start_state[self.action['pick']] != "table":
                #If the object is not on the table
                line = f"(unstack {self.action['pick']} {start_state[self.action['pick']]})"
                f.write(line)
                pick_action = 'unstack'
            elif start_state[self.action['pick']] == "table":
                print("PENIS")
                line = f"(pick-up {self.action['pick']})"
                f.write(line)
                pick_action = 'pick-up'
            else:
                pass
            if end_state[self.action['pick']] != "table":
                #If the object is not going to be placed on the table
                line = f"\n(stack {self.action['pick']} {end_state[self.action['pick']]})"
                f.write(line)
                place_action = 'stack'
            elif end_state[self.action['pick']] == "table":
                print("DOUBLE PENIS")
                line = f"\n(put-down {self.action['pick']})"
                f.write(line)
                place_action = 'put-down'
        return pick_action, place_action
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
        names = problem.name
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
        return initial_placement_map, final_placement_map, names

class ActionOperator(Action):
    def __init__(self, domain_file, problem_file, action_object: Action, output_path, pick_action:bool):
        super().__init__(problem_file, action_object.action, output_path)
        self.domain_file = domain_file
        self.problem_file = problem_file
        self.action = action_object
        self.action_binds = action_object.operator_binds
        self.output_path = output_path
        self.pick_action = pick_action
        self.parser = Parser(domain_file, problem_file)

        self.deparam_action_preconditions, self.deparam_add_effects, self.deparam_del_effects = self.__get_action_preconditions__()
        self.deparam_action_preconditions = self.__substitute_params__(set(self.deparam_action_preconditions))
        self.deparam_add_effects = self.__substitute_params__(set(self.deparam_add_effects))
        self.deparam_del_effects = self.__substitute_params__(set(self.deparam_del_effects))
        self.state_preconditions = self.__get_state_preconditions__()

        self.action_operator = Operator(self.action.name, self.deparam_action_preconditions, self.deparam_add_effects, self.deparam_del_effects)
        pyperplan_compliant = self.action_operator.applicable(self.state_preconditions)
        print(f"Pyperplan compliant: {pyperplan_compliant}")
        if not pyperplan_compliant:
            raise BadModelPrediction()

    def __get_action_preconditions__(self):
        domain_parsed = self.parser.parse_domain(True)
        for action_name, dom_action in domain_parsed.actions.items():
            if (self.action.pick_action != action_name) if self.pick_action else (self.action.place_action != action_name):
                continue
                # Skips to next
            else:
                add_effect = frozenset(dom_action.effect.addlist)
                del_effect = frozenset(dom_action.effect.dellist)
                precondition = frozenset(dom_action.precondition)
                # Pyperplan expecting hashable, immutable type, so I just use a frozenset.
                return precondition, add_effect, del_effect
        return frozenset(), frozenset(), frozenset()
    #TODO Fix ussue in here.
    def __get_state_preconditions__(self):
        action_preconditions, _, _ = self.__get_action_preconditions__()
        #Parsing non-parameterized state preconditions
        domain_parsed = self.parser.parse_domain(read_from_file=True)
        problem_parsed = self.parser.parse_problem(domain_parsed, read_from_file=True)
        #Parses domain for problem
        updated_preconditions = set()
        state_preconditions = set(problem_parsed.initial_state)
        for precondition in state_preconditions:
            updated_preconditions.add(str(precondition))
            continue
        return updated_preconditions

    def __substitute_params__(self, input_set: set):
        updated_set = set()
        for item in input_set:
            item = str(item).replace('?x', self.action_binds['?x'])
            item = str(item).replace('?y', self.action_binds['?y'])
            item = str(item).replace('[object]', 'object')
            updated_set.add(ast.literal_eval(item)) if type(item) is not str else updated_set.add(item)
        return updated_set
#TODO Add handling of ?y variable if table is one of the blocks because otherwise the code will break
if __name__ == "__main__":
    example_action = "pick: yellow_block place: blue_block"
    ba = Action('problem.pddl', example_action, 'hehe.pddl.soln')
    print(ba.__parse_action__(example_action))
    print(ba.get_operator_bindings())
    print(ba.__write_action_operator__())
    ao = ActionOperator('domain.pddl', problem_file='problem.pddl', action_object=ba, pick_action=True, output_path=ba.output_path)
    print(ao.__get_action_preconditions__())
    print(ao.__get_state_preconditions__())

