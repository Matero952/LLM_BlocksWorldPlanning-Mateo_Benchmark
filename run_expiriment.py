from prompts import get_basic_prompt
import pandas as pd
from APIKeys import API_KEY
from experiment import Experiment
from openai import OpenAI
import json
import os



def run_experiment(model, prompt):
    print(f"\n\n\n\nbegining to run experiment {model=} {prompt=}")
    df = pd.read_csv('./ground_truth.csv')
    client = OpenAI(
        api_key= API_KEY,
    )
    
    if prompt == "basic_prompt":
        prompt_func = get_basic_prompt

    exp = Experiment(model, prompt_func, client)

    save_dir = os.path.join("./results", f'{model}_{prompt}/')
    os.makedirs(save_dir, exist_ok=True)

    new_df = pd.DataFrame(columns=['start_state', 'end_state', 'next_best_move', 'predicted_next_best_move', "response"])
    newdf_path = os.path.join(save_dir, f'{model}_{prompt}results.csv')

    correct = 0
    seen = 0
    for index, row in df.iterrows():
        start_state = json.loads(row['start_state'])
        end_state = json.loads(row['end_state'])
        label = json.loads(row['next_best_move'])
        response, pred = exp.process_sample(start_state, end_state)
        correct += 1 if pred == label else 0
        seen += 1
        new_df.loc[len(new_df)] = [json.dumps(start_state), json.dumps(end_state), json.dumps(label), json.dumps(pred), response]
        print(f"\rProcessing: {index+1}/{len(df)}, accuracy:{correct/seen} ({correct} / {seen})" , end="")
        new_df.to_csv(newdf_path, index = False)


if __name__ =="__main__":
    run_experiment("gpt-4o-2024-11-20",  "basic_prompt")