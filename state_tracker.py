import ast
import regex as re
from pyperplan.task import Operator
from pyperplan.pddl.parser import Parser


class ActionOperator:
    """Taking better name suggestions please."""
    def __init__(self, state: tuple, action: str, domain_file: str, problem_file: str, formatted_action_file: str) -> None:
        self.state = state
        self.action = action
        self.domain_file = domain_file
        self.problem_file = problem_file
        self.formatted_action_file = formatted_action_file
    def get_action_information(self):
        """Writes a file that takes transforms an action like
        "{""pick"": ""red_block"", ""place"": ""yellow_block""}"
        into a pyperplan compliant operator.
        """
        formed_state = self.state[0]
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
        assert type(self.action) == str, 'Action must be a string(1)'
        formed_action = re.sub(r'(\w+): (\w+)', r"'\1': '\2'", self.action)
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
        # TODO Fix this monstrosity
        print(f"Unstackable: {unstackable}, pick_upable: {pick_upable}")
        with open(self.formatted_action_file, 'w') as f:
            if formed_action['pick'] in pick_upable:
                f.write(f"(pick-up {formed_action['pick']})")
            else:
                f.write(f"\n(unstack {formed_action['pick']})" + ')')
            if formed_action['place'] == 'table':
                f.write(f"\n(put-down {formed_action['pick']}" + ')')
            else:
                f.write(f"\n(stack {formed_action['pick']} {formed_action['place']}" + ')')
        return None
    def get_domain_information(self) -> tuple[frozenset, frozenset, frozenset] or None:
        """Retrieves action preconditions, add effects, and del effects."""
        assert (type(self.domain_file) == str and type(self.problem_file) == str and
                type(self.formatted_action_file) == str)
        # Files must be strings
        with open(self.formatted_action_file, 'r') as f:
            first_line = f.readline().strip()
            found_action = re.search(r"\(\s*(\S+)", first_line).group(1)
            print(f"Action1: {found_action}")
            # Extracting action from format_action
            if not found_action:
                raise ValueError("Action isnt valid.")
            # Action must be valid yk
        parser = Parser(self.domain_file, self.problem_file)
        domain_parsed = parser.parse_domain(read_from_file=True)
        for action_name, action in domain_parsed.actions.items():
            if found_action != action_name:
                continue
                # Skips to next
            else:
                add_effect = frozenset(action.effect.addlist)
                del_effect = frozenset(action.effect.dellist)
                precondition = frozenset(action.precondition)
                # Pyperplan expecting hashable, immutable type, so I just use a frozenset.
                return precondition, add_effect, del_effect
                # Return values are used for making Operator object.
    def get_state_preconditions(self) -> frozenset:
        parser = Parser(self.domain_file, self.problem_file)
        domain_parsed = parser.parse_domain(read_from_file=True)
        problem_parsed = parser.parse_problem(domain_parsed, read_from_file=True)
        print(f"Problem: {problem_parsed} typd: {type(problem_parsed)}")
        preconditions = problem_parsed.goal
        #Which dumbass refers to preconditions as goal wtffff
        print(f"preconditions: {preconditions}")
        return frozenset(preconditions)
    def get_missing_preconditions(self) -> None:
        preconditions, _, _  = self.get_domain_information()
        print(f"preconditions: {preconditions}")
        missing_preconditions = preconditions - self.get_state_preconditions()
        print(f"missing_preconditions: {missing_preconditions}")

    def get_state_prime(self) -> None:
        return None
    def apply_operator(self, operator: Operator):
        extracted_state = (self.state[1])
        # Problem is that state is not in the same format as operator
        # Problem is that state needs preconditions
        print(f"Preconditions: {operator.preconditions}")
        missing_conditions = operator.preconditions - extracted_state
        print(f"Missing conditions: {missing_conditions}")
        op_applicable = operator.applicable(extracted_state)
        # Checks if the operator is applicable
        print(f"Operator applicable: {op_applicable}")
        if not op_applicable:
            raise ValueError("Operator is unapplicable")
        else:
            state_prime = operator.apply(extracted_state)
            # Applies operator to state
        print(f"Old state: {extracted_state}, new state: {state_prime}.")
        return state_prime

if __name__=='__main__':
    example_action = "{""pick"": ""red_block"", ""place"": ""yellow_block""}"
    example_state = "{""red_block"": ""table"", ""blue_block"": ""table"", ""yellow_block"": ""table""}","{""red_block"": ""table"", ""blue_block"": ""table"", ""yellow_block"": ""table""}","{""pick"": ""None"", ""place"": ""None""}","""0"""
    ao = ActionOperator(state=example_state, action=example_action, domain_file='domain.pddl',
                        problem_file='problem.pddl', formatted_action_file='hehe.pddl.soln')
    precondiditons = ao.get_state_preconditions()
    print(f"precondiditons: {precondiditons}")
    ao.get_missing_preconditions()