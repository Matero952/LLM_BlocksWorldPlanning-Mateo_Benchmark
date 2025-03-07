import ast
import regex as re
from pyperplan.task import Operator
from pyperplan.pddl.parser import Parser, Predicate


#TODO Parameterize '?y'
class ActionOperator:
    """Taking better name suggestions please."""
    def __init__(self, state: tuple, action: str, domain_file: str, problem_file: str, formatted_action_file: str) -> None:
        self.state = state
        self.action = action
        self.domain_file = domain_file
        self.problem_file = problem_file
        self.formatted_action_file = formatted_action_file

    def get_action_information(self):
        """Writes a file that transforms an action like
        "{""pick"": ""red_block"", ""place"": ""yellow_block""}"
        into a pyperplan compliant operator.
        """
        formed_state = self.state[0]
        formed_state = (re.sub(r'(\w+):\s*(\w+)', r"'\1': '\2'", formed_state))
        formed_state = ast.literal_eval(formed_state)
        assert type(formed_state) == dict, "Formed_state is not a dict"
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
                f.write(f"(unstack {formed_action['pick']})" + ')')
            if formed_action['place'] == 'table':
                f.write(f"\n(put-down {formed_action['pick']}" + ')')
            else:
                f.write(f"\n(stack {formed_action['pick']} {formed_action['place']}" + ')')
        return formed_action['pick'], formed_action['place']
    def get_domain_information(self) -> tuple[frozenset, frozenset, frozenset] or None:
        """Retrieves action preconditions, add effects, and del effects."""
        assert (type(self.domain_file) == str and type(self.problem_file) == str and
                type(self.formatted_action_file) == str)
        # Files must be strings
        with open(self.formatted_action_file, 'r') as f:
            first_line = f.readline().strip()
            found_action = re.search(r"\(\s*(\S+)", first_line)
            # Extracting action from format_action
            if not found_action:
                raise ValueError("Action isnt valid.")
            else:
                found_action = found_action.group(1)
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
        preconditions = frozenset(problem_parsed.initial_state)
        return preconditions
    def get_operator_bindings(self, b1, b2) -> dict:
        """Action predicates are naturally parameterized.
        This function retrieves the parameters based on some pddl logic."""
        #Blocks are clear if there is nothing above them, which means that the block
        #being picked up needs to be clear, which is our ?x variable. Our y variable
        #is just our other block
        op_bindings = {}
        x_var, y_var = self.get_action_information()
        op_bindings[b1] = x_var
        op_bindings[b2] = y_var
        #Variables we found earlier.
        op_bindings['[object]'] = 'object'
        print(f"Operator bindings: {op_bindings}")
        return op_bindings

    @staticmethod
    def sort_preconds(action_precond, state_precond):
        action_predicate_list = list(action_precond)
        action_predicate_list_sorted = sorted(action_predicate_list, key=lambda x: x.name)
        state_predicate_list = list(state_precond)
        state_predicate_list_sorted = sorted(state_predicate_list, key=lambda x: x.name)
        print(f"action_predicate_list_sorted: {action_predicate_list_sorted}")
        print(f"state_predicate_list_sorted: {state_predicate_list_sorted}")
        return action_predicate_list_sorted, state_predicate_list_sorted
    def remove_parameters(self, pa, pb, pc) -> list:
        #Goal here is to plug in values for sorted_action_precons
        print(f"pa: {pa}, pb: {pb}, pc: {pc}")
        action_preconditions, _, _ = self.get_domain_information()
        sorted_action_precons, _ = self.sort_preconds(action_preconditions, self.get_state_preconditions())
        op_bindings = self.get_operator_bindings(pa, pb)
        print(f"Operator bindings: {op_bindings}")
        assert type(sorted_action_precons) == list
        for index, entry in enumerate(sorted_action_precons):
            print(f"entry: {entry}, type: {type(entry)}")
            if pa in str(entry):
                sorted_action_precons[index] = str(entry).replace("\\", "")
                print(f"Sorting action_precons[index]: {sorted_action_precons[index]}, type; {type(sorted_action_precons[index])}")
                sorted_action_precons[index] = sorted_action_precons[index].replace(f"{pa}", f"{op_bindings[pa]}")
                print(f"Sorted action_precons[index]: {sorted_action_precons[index]}")
            if pb in str(entry):
                sorted_action_precons[index] = str(entry).replace("\\", "")
                print(
                    f"Sorting action_precons[index]: {sorted_action_precons[index]}, type; {type(sorted_action_precons[index])}")
                sorted_action_precons[index] = sorted_action_precons[index].replace(f"{pb}", f"{op_bindings[pb]}")
                print(f"Sorted action_precons[index]: {sorted_action_precons[index]}")
            if pc in str(entry):
                sorted_action_precons[index] = str(entry).replace("\\", "")
                print(
                    f"Sorting action_precons[index]: {sorted_action_precons[index]}, type; {type(sorted_action_precons[index])}")
                sorted_action_precons[index] = sorted_action_precons[index].replace(f"{pc}", f"{op_bindings[pc]}")
                print(f"Sorted action_precons[index]: {sorted_action_precons[index]}")
        print(f"Sorted action_precons: {sorted_action_precons}")
        return sorted_action_precons
    def plug_parameters(self, action_predcon: list, bdict: dict, pA, pB, pC):
        """Meant to be called on a single string."""
        #Just add more variables for future, more complicated worlds.
        action_predcon_sorted, _ = self.sort_preconds(action_predcon)
        pA = pA.replace("\\", "")
        pB = pB.replace("\\", "")
        pC = pC.replace("\\", "")
        print(f"PA: {pA}")
        print(f"Typel actionpredcon: {type(action_predcon)}")
        deparamed_action_preda = re.sub(pA, bdict[pA], action_predcon)
        deparamed_action_predb = re.sub(pB, bdict[pB], deparamed_action_preda)
        deparamed_action_predc = re.sub(pC, bdict[pC], deparamed_action_predb)
        print(f"deparamed_action_pred: {deparamed_action_predc}")
        return deparamed_action_predc





    def get_missing_preconds(self, action_preconditions, state_preconditions):
        numb_precons = len(action_preconditions)
        cleared_precons = set()
        missing = set()
        #Using a set for no duplicate values.
        for index, precon in enumerate(action_preconditions):
            print(f"Type:heeh {type(precon)}")
            action_preconditions[index] = self.plug_parameters(precon, self.get_operator_bindings('?x', '?y'), r"\?x", r"\?y", r"\object")
        #Fix action preconditions
        for action_precondition in action_preconditions:
            if action_precondition not in state_preconditions:
                missing.add(action_precondition)
            else:
                cleared_precons.add(action_precondition)
        return missing, cleared_precons

    def get_state_prime(self) -> None:
        return None
    def apply_operator(self, operator: Operator):
        extracted_state = (self.state[1])
        missing_conditions = operator.preconditions - extracted_state
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
    example_state = "{""red_block"": ""blue_block"", ""blue_block"": ""table"", ""yellow_block"": ""table""}","{""red_block"": ""yellow_block"", ""blue_block"": ""table"", ""yellow_block"": ""table""}","{""pick"": ""None"", ""place"": ""None""}","""0"""
    ao = ActionOperator(state=example_state, action=example_action, domain_file='domain.pddl',
                        problem_file='problem.pddl', formatted_action_file='hehe.pddl.soln')
    state_preconditions = ao.get_state_preconditions()
    action_predicates, _, _ = ao.get_domain_information()
    action_predicates, state_predicates = ao.sort_preconds(action_predicates, state_preconditions)
    ao.remove_parameters('?x', '?y', '[object]')




