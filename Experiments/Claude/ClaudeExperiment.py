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
        self.model_name = model

    def process_sample(self, start, end):
        prompt = self.prompt_func(start, end)
        response = self.client.messages.create(
            max_tokens=1000,
            model = self.model,
            messages = [{
                "role" : "user",
                "content" : prompt}])
        print(f"Response: {response}")
        result = response.content[0].text
        print(f"Response: {result}")
        pick_match = re.search(r"(?i)pick\s*:\s*(.*)", result)
        print(f"Pick match: {pick_match}")
        place_match = re.search(r"(?i)place\s*:\s*(.*)", result)
        print(f"Place match: {place_match}")
        pick_str = pick_match.group(1).strip()
        print(f"Pick string: {pick_str}")
        place_str = place_match.group(1).strip()
        print(f"Place string: {place_str}")
        output = {"pick": pick_str, "place": place_str}
        return result, output

if __name__ == "__main__":
    from prompts import get_basic_prompt
    import pandas as pd
    import json
    model = "claude-3-5-haiku-latest"
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
