import re
import DSConstants as DS
from DSConstants import OPENAI as OpenAI

class DSExperiment:

    def __init__(self, model, prompt_func):
        self.model_name = model
        self.prompt_function = prompt_func
        self.client = OpenAI(api_key = f"{DS.API_KEY}", base_url = "https://api.deepseek.com")
        #Replace this line above with the actual thing

    def process_sample(self, start, end):
        prompt = self.prompt_function(start, end)
        response = self.client.chat.completions.create(
            model=  "deepseek-chat",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                    ]
                },
            ],
        )
        result = response.choices[0].message.content
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
    model = f"{DS.DS_CHAT}"
    #Deepseek v3
    print(model)
    experiment_4o = DSExperiment(model, get_basic_prompt)
    df = pd.read_csv('./ground_truth.csv')
    row = df.sample(n=1).iloc[0]
    start_state = json.loads(row['start_state'])
    end_state = json.loads(row['end_state'])
    label = json.loads(row['next_best_move'])
    result, pred = DSExperiment.process_sample(start_state, end_state)
    print(f"{start_state=}")
    print(f"{end_state=}")
    print(f"{pred=}")
    print(f"{label=}")
    print(f"{result=}")
    print(f"{pred == label}")


    