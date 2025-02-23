import re
import json
from dotenv import load_dotenv
import os
load_dotenv()
dotenv_path = '/home/mateo/Github/LLM_Blocks-Mateo/.env'
load_dotenv(dotenv_path)

import os
from openai import OpenAI

class grokexperiment:
    def __init__(self, model, prompt_function):
        self.model = model
        self.client = OpenAI(api_key=os.getenv("GROK_API_KEY"), base_url="https://api.x.ai/v1")
        self.prompt_func = prompt_function
        self.model_name = model
    def process_sample(self, start, end):
        prompt = self.prompt_func(start, end)
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role" : "user",
                 "content" : prompt}
            ]
        )
        result = completion.choices[0].message.content
        pick_match = re.search(r"(?i)pick\s*:\s*(.*)", result)
        place_match = re.search(r"(?i)place\s*:\s*(.*)", result)
        pick_str = pick_match.group(1).strip()
        place_str = place_match.group(1).strip()
        output = {"pick": pick_str, "place": place_str}
        return result, output

if __name__ == "__main__":
    from prompts import get_basic_prompt
    import pandas as pd
    import json
    model = f"grok-2-latest"
    print(model)
    experiment_GEM = grokexperiment(model, get_basic_prompt)
    df = pd.read_csv('../../ground_truth.csv')
    row = df.sample(n=1).iloc[0]
    start_state = json.loads(row['start_state'])
    end_state = json.loads(row['end_state'])
    label = json.loads(row['next_best_move'])
    result, pred = experiment_GEM.process_sample(start_state, end_state)
    print(f"{start_state=}")
    print(f"{end_state=}")
    print(f"{pred=}")
    print(f"{label=}")
    print(f"{result=}")
    print(f"{pred == label}")
