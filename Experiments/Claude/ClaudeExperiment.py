import re as re
from dotenv import load_dotenv
import os
import anthropic
load_dotenv()
dotenv_path = '/home/mateo/Github/LLM_Blocks-Mateo/.env'
load_dotenv(dotenv_path)

class ClaudeExperiment:
    def __init__(self, model, prompt_function):
        self.client = anthropic.Anthropic(api_key=os.getenv('CLAUDE'))
        self.model = model
        self.prompt_func = prompt_function

    def process_sample(self, start, end):
        prompt = self.prompt_func(start, end)
        response = self.client.messages.create(
            max_tokens=1000,
            model = self.model,
            #TODO Check to make sure this is the correct parameter
            messages = [
                prompt
            ]
        )
        print(f"Response: {response}")
        pick_match = re.search(r"(?i)pick\s*:\s*(.*)", result)
        place_match = re.search(r"(?i)place\s*:\s*(.*)", result)
        pick_str = pick_match.group(1).strip()
        place_str = place_match.group(1).strip()
        output = {"pick": pick_str, "place": place_str}
        return result, output
        #TODO Figure out how to call claude with our API but like I dont want to pay money ):
if __name__ == "__main__":
    from prompts import get_basic_prompt
    import pandas as pd
    import json
    model = "anthropic.claude-3-opus-20240229-v1:0"
    print(model)
    experiment = ClaudeExperiment(model, get_basic_prompt)
    df = pd.read_csv('../../ground_truth.csv')
    row = df.sample(n=1).iloc[0]
    start_state = json.loads(row['start_state'])
    end_state = json.loads(row['end_state'])
    label = json.loads(row['next_best_move'])
    result = experiment.process_sample(start= start_state, end= end_state)
    print(f"{start_state=}")
    print(f"{end_state=}")
    print(f"{label=}")
    print(f"{result=}")
