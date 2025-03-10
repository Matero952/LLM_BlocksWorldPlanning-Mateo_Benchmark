import re
from os import environ
import google.generativeai as genai
from google.ai.generativelanguage_v1 import GenerateContentResponse
import json
from dotenv import load_dotenv
import os
load_dotenv()
dotenv_path = '/home/mateo/Github/LLM_Blocks-Mateo/.env'
load_dotenv(dotenv_path)


class GEMExperiment:

    def __init__(self, model, prompt_function):
        self.model = genai.GenerativeModel(model)
        genai.configure(api_key=os.getenv("GEMINI"))
        self.prompt_func = prompt_function
        self.model_name = model

    def process_sample(self, start, end):
        prompt = self.prompt_func(start, end)
        response = self.model.generate_content(
            prompt

            # prompt = prompt
            # messages = [
            #     {
            #         "role": "user",
            #         "content": [
            #             {"type": "text", "text": prompt},
            #         ]
            #     },
            # ],
        )
        result = response.candidates[0].content.parts[0].text
        #Figured it out (:
        # result = data["candidates"][0]["message"]["content"]
        # result = GenerateContentResponse.candidates[0]
        #response.candidates[0].message.content

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
    model = f"gemini-1.5-flash"
    print(model)
    experiment_GEM = GEMExperiment(model, get_basic_prompt)
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
