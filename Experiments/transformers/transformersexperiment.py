import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import re
import pandas as pd
import json as json
import os
from transformers import pipeline

class transformersexperiment:
    def __init__(self, model, prompt_func):
        self.model = model
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.prompt_func = prompt_func
        self.model_name = model
    def process_sample(self, start, end):
        print(f"1")
        prompt = self.prompt_func(start, end)
        print(f"2")
        messages = [
            {"role" : "user",
             "content": prompt}
        ]
        pipe = pipeline("text-generation", model="Qwen/Qwen1.5-72B")
        result = pipe(messages)
        print(f"Result: {result}")
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
    print('Starting experiment...')
    model = "Qwen/Qwen1.5-72B"
    print(f"Model: {model}")
    experiment = transformersexperiment(model=model, prompt_func=get_basic_prompt)
    df = pd.read_csv('../../ground_truth.csv')
    row = df.sample(n=1).iloc[0]
    start_state = json.loads(row['start_state'])
    end_state = json.loads(row['end_state'])
    label = json.loads(row['next_best_move'])
    result, pred = experiment.process_sample(start=start_state, end=end_state)
    print(f"{start_state=}")
    print(f"{end_state=}")
    print(f"{label=}")
    print(f"{result=}")

