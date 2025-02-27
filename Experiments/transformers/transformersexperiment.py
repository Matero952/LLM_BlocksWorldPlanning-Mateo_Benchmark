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
        # self.device = torch.device('cpu')
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.prompt_func = prompt_func
        self.model_name = model
        self.pipe = pipeline("text-generation", model=self.model, max_new_tokens=1500, device=self.device, temperature=0.5)
        #Temperature here was 0.6 but i changed it to 0.5 because model outputs were just rambling.
        self.pattern = r"(red|yellow|blue|table|None|none)"
        self.pattern_mapping = {"red": "red_block", "yellow": "yellow_block", "blue": "blue_block", "table": "table",
                           "none": "None"}
        self.max_retries = 5
    def process_sample(self, start, end):
        pick_match, place_match, result = self.get_valid_output(start, end)
        try:
            pick_match = (re.search(self.pattern, pick_match)).group(1).lower()
            place_match = (re.search(self.pattern, place_match)).group(1).lower()
        except AttributeError:
            print(f"Pick_match: {pick_match}, place_match: {place_match}")
            print(f"Result: {result}")
            raise Exception("No match found.")
        print(f"Pick match group 1: {pick_match}")
        print(f"Pick match group 1 type: {type(pick_match)}")
        print(f"Place match group 1: {place_match}")
        print(f"Place match group 1 type: {type(place_match)}")
        cleaned_pick_str = self.pattern_mapping.get(pick_match)
        cleaned_place_str = self.pattern_mapping.get(place_match)
        print(f"pick_match: {pick_match}", f"place_match: {place_match}")
        output = {"pick": cleaned_pick_str, "place": cleaned_place_str}
        print(f"output: {output}")
        return result, output
    def get_valid_output(self, start, end, retry_count=0):
        if retry_count > self.max_retries:
            raise Exception(f"Max retries exceeded: {retry_count}")
        prompt = self.prompt_func(start, end)
        messages = [
            {"role": "user",
             "content": prompt}
        ]
        try:
            respone = self.pipe(messages)
            print(f"This message indicates that the model's response was not valid."
                  f"As I am using recursion here, I have a maximum depth set to: {self.max_retries}")
            result = respone[0]['generated_text'][1]['content']
            # result = respone[0]['generated_text']
            print(f"Result: {result}")
            pick_match = (re.search(r"(?i)pick\s*:\s*(.*)", result)).group(1).lower()
            place_match = (re.search(r"(?i)place\s*:\s*(.*)", result)).group(1).lower()
        except AttributeError:
            return self.get_valid_output(start, end, retry_count + 1)
        valid_pick_output = pick_match
        valid_place_output = place_match
        print(f"valid_pick_output: {valid_pick_output}", f"valid_place_output: {valid_place_output}, result: {result}")
        return valid_pick_output, valid_place_output, result
if __name__ == "__main__":
    from prompts import get_basic_prompt
    print('Starting experiment...')
    model = "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B"
    print(f"Model: {model}")
    experiment = transformersexperiment(model=model, prompt_func=get_basic_prompt)
    df = pd.read_csv('../../ground_truth.csv')
    row = df.iloc[3]
    # row = df.sample(n=1).iloc[0]
    start_state = json.loads(row['start_state'])
    end_state = json.loads(row['end_state'])
    label = json.loads(row['next_best_move'])
    result, pred = experiment.process_sample(start=start_state, end=end_state)
    print(f"{start_state=}")
    print(f"{end_state=}")
    print(f"{label=}")
    print(f"{result=}")
    print(f"Correct Qwen!") if pred==label else print(f"Wrong Qwen!")