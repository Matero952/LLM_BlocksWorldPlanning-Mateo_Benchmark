from typing import Optional
from pyperplan.pddl.parser import Parser
from tests.ComplexTestCases import ComplexTestCases

class OutputParser:
    def __init__(self, domain_pddl, problem_pddl: str, keyword1: str, keyaction1: str, keyword2: Optional[str]=None, keyword3: Optional[str]=None, keyword4: Optional[str]=None, keyword5: Optional[str]=None, keyaction2: Optional[str]=None, keyaction3: Optional[str]=None):
        #Add more keywords for more complex worlds if necessary
        self.domain_pddl = domain_pddl
        self.problem_pddl = problem_pddl

        self.keywords = [keyword for keyword in (keyword1, keyword2, keyword3, keyword4, keyword5) if keyword is not None]
        self.keyactions = [keyaction for keyaction in (keyaction1, keyaction2, keyaction3) if keyaction is not None]
        #Doing this as some parameters are initialized to none and will mess up parse func if they stay in string.

        self.parser = Parser(domain_pddl, problem_pddl)
        self.domain_parsed = self.parser.parse_domain(True)
        self.objects = (self.parser.parse_problem(self.domain_parsed, True)).objects

    def parse(self, model_output, word_tolerance: int, line_tolerace: int):
        #Word tolerance is max distance between keyaction and keyword
        model_output = str(model_output) if type(model_output) is not str else model_output
        filtered_output = self.extract_target_lines(model_output, line_tolerace)
        all_tokens_list = []
        print(f"Filtered_output: {filtered_output}")
        for output in filtered_output:
            tokens = output.split()
            print(f"Tokens: {tokens}")
            all_tokens_list.append(tokens)
        actions = self.get_matches(all_tokens_list, word_tolerance, self.keyactions, self.keywords, 2)
        if actions:
            #Checks if list is empty
            return actions
        else:
            return [{'pick': 'None'}, {'place': 'None'}]
        #Please redo this last part

    @staticmethod
    def check_match_tolerance(keyword: str, token: str):
        #Basically checks accuracy between keyword and token
        if keyword != 'None':
            #Handling of when token 'on' was in 'None' and returned true
            try:
                first_part, second_part = keyword.split('_', 1)
            except ValueError:
                first_part = keyword
            if first_part in token:
                return True
            else:
                return False
        else:
            return True if token == 'None' else False

    @staticmethod
    def extract_target_lines(model_output, line_tolerance):
        assert type(model_output) == str
        target_lines = model_output.splitlines()[-line_tolerance:]
        print(target_lines)
        #Only keeps the index 'line_tolerance' to the end
        while '' in target_lines:
            target_lines.remove('')
        #Remove empty values
        return target_lines

    def get_matches(self, all_tokens_list: list, word_tolerance: int, actions: list, keywords: list, max_count: int):
        action_word_list = []
        for token_list in all_tokens_list:
            for index, token in enumerate(token_list):
                for action in actions:
                    if action in token:
                        for keyword in keywords:
                            if self.check_match_tolerance(keyword, ' '.join(token_list[index:index + word_tolerance])):
                                action_word_map = {action : keyword}
                                action_word_list.append(action_word_map)
                                print(f"Tokens: {token_list[index:index + word_tolerance]}")
                                print("BINGO")
        return action_word_list[:max_count]

if __name__ == "__main__":
    op = OutputParser('../domain.pddl', '../problem.pddl', keyword1='table', keyaction1='pick', keyword2='red_block', keyword3='yellow_block', keyword4='blue_block', keyword5='None', keyaction2='place')
    #TODO Run test cases in enum test cases and add handling of 'table' object but other its good i think (:
    string = ComplexTestCases.TEST5.value
    print(op.parse(string, 3, 3))
