import re
class Experiment:
    def __init__(self, model_name, prompt_function, client):
        self.model_name = model_name
        self.prompt_function = prompt_function
        self.client = client

    def process_sample(self, start_state, end_state):
        prompt = self.prompt_function(start_state, end_state)
        response = self.client.chat.completions.create(
            model=self.model_name,
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
        try:
            pick_match = re.search(r"pick: \s*(.*)", result)
            place_match = re.search(r"place: \s*(.*)", result)
            pick_str = pick_match.group(1).strip()
            place_str = place_match.group(1).strip()
        except:
            pick_str = "error"
            place_str = "error"
        
        output = {"pick": pick_str, "place": place_str}
        return result, output, 
        

if __name__ == "__main__":
    from prompts import get_basic_prompt
    import pandas as pd
    from APIKeys import API_KEY
    from openai import OpenAI
    import json

    client = OpenAI(
        api_key= API_KEY,
    )


    print(f"GPT_4o")
    experiment_4o = Experiment("gpt-4o-2024-11-20", get_basic_prompt, client)
    df = pd.read_csv('./ground_truth.csv')

    row = df.sample(n=1).iloc[0]
    start_state = json.loads(row['start_state'])
    end_state = json.loads(row['end_state'])
    label = json.loads(row['next_best_move'])
    pred = experiment_4o.process_sample(start_state, end_state)
    print(f"{start_state=}")
    print(f"{end_state=}")
    print(f"{pred=}")
    print(f"{label=}")
    print()
    assert pred == label

    print(f"GPT_o1")
    experiment_o1 = Experiment("o1-preview", get_basic_prompt, client)

    row = df.sample(n=1).iloc[0]
    start_state = json.loads(row['start_state'])
    end_state = json.loads(row['end_state'])
    label = json.loads(row['next_best_move'])
    pred = experiment_o1.process_sample(start_state, end_state)
    print(f"{start_state=}")
    print(f"{end_state=}")
    print(f"{pred=}")
    print(f"{label=}")
    print()

