from Experiments.Gemini.GEMExperiment import GEMExperiment
from prompts import get_basic_prompt
import pandas as pd
import json
import os
import time
import regex as re
import matplotlib.pyplot as plt
from Experiments.transformers.transformersexperiment import transformersexperiment
from Experiments.Claude.ClaudeExperiment import ClaudeExperiment
from Experiments.grok.grokexperiment import grokexperiment
import torch


"""
This module runs an experiment using a specified model and prompt function, processes a dataset of ground truth values, 
and saves the results to a CSV file.

Functions:
    run_experiment(experiment, suffix=""):
        Runs the experiment with the given model and prompt function, processes each sample in the dataset, 
        and saves the results to a CSV file.

Classes:
    OAI_Experiment:
        A class representing the experiment to be run, which includes methods for processing samples.

Modules:
    prompts:
        Contains functions for generating prompts.
    experiments:
        Contains the OAI_Experiment class and other related functionalities.
"""

def run_experiment(experiment, ground_truth_csv_path, suffix=""):
    """
    Runs the experiment with the given model and prompt function, processes each sample in the dataset, 
    and saves the results to a CSV file.

    Args:
        experiment (OAI_Experiment): An instance of the OAI_Experiment class, which includes the model and prompt function to be used.
        suffix (str, optional): A suffix to be added to the results directory and file names. Defaults to "".

    Returns:
        accuracy: float
    """
    torch.cuda.empty_cache()
    quotas = {"gemini-2.0-flash-exp": 5.01, "gemini-1.5-flash": 4.01, "gemini-2.0-flash-001": 4.01,
              "gemini-2.0-flash-lite-preview-02-05": 4.01, "gemini-1.5-pro": 33, "claude-3-5-haiku-latest" : 0,
              "claude-3-5-sonnet-20241022" : 0, "grok-2-latest" : 0, "grok-2" : 0,
              "grok-beta" : 0, "grok-2-vision" : 0, "grok-2-vision-latest" : 10, "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B" : 0, "claude-3-7-sonnet-20250219" : 0, "deepseek-ai/DeepSeek-R1-Distill-Llama-8B" : 0}
    if experiment.model_name not in quotas.keys():
        print(f"Error: {experiment.model_name} is not a valid model name.")
    model_name = transformer_name(experiment.model_name)
    print(f"Experiment name: {model_name}")
    print(f"\n\n\n\nbeginning to run experiment {model_name} {experiment.prompt_func=}")
    df = pd.read_csv(ground_truth_csv_path)
    os.makedirs("./results/", exist_ok=True)
    print(f"Model name: {model_name}")
    save_dir = os.path.join("./results/", model_name + f"{suffix}/")
    # save_dir = os.path.join("./results/", re.search(r'[^()/]+$',experiment.model_name) + f"{suffix}/'")
    # save_dir = os.path.join("./results/", f'{re.sub(r'.*/', '', experiment.model_name)}{suffix}/')
    os.makedirs(save_dir, exist_ok=True)
    newdf_path = os.path.join(save_dir, f'{model_name}{suffix}_results.csv')
    if os.path.exists(newdf_path):
        new_df = pd.read_csv(newdf_path)
    else:
        new_df = pd.DataFrame(
            columns=['start_state', 'end_state', 'next_best_move', 'predicted_next_best_move', "response"])
        print(f"Created new dataframe")
    correct = 0
    seen = 0
    for index, row in df.iterrows():
        model_quota = quotas[f"{experiment.model_name}"]
        start_state = json.loads(row['start_state'])
        end_state = json.loads(row['end_state'])
        label = json.loads(row['next_best_move'])
        if (index < len(new_df) and
            new_df.at[index, 'start_state'] == json.dumps(start_state) and
            new_df.at[index, 'end_state'] == json.dumps(end_state)):
            model_quota = 0
            checking = True
            if new_df.at[index, 'predicted_next_best_move'] == json.dumps(label):
                print("Checking!")
                match = True
                correct += 1
                seen += 1
            else:
                correct += 0
                seen += 1
            time.sleep(model_quota)
            print(f"Checking row {index + 1}/{len(df)}: {row.to_dict()}")
        else:
            response, pred = experiment.process_sample(start_state, end_state)
            print("Processing!")
            print(f"Processing row {index + 1}/{len(df)}: {row.to_dict()}")
            correct += 1 if pred == label else 0
            seen += 1
            new_df = pd.concat([new_df, pd.DataFrame(
                [[json.dumps(start_state), json.dumps(end_state), json.dumps(label), json.dumps(pred), response]],
                columns=['start_state','end_state','next_best_move','predicted_next_best_move',"response"])],
                               ignore_index=True)
        print(f"\rProcessing: {index + 1}/{len(df)}, accuracy:{correct / seen} ({correct} / {seen}, model: {experiment.model_name})", end="")
        new_df.to_csv(newdf_path, index=False)
        time.sleep(model_quota)
    with open(os.path.join(save_dir, f'{model_name}{suffix}_accuracy.txt'), 'w') as f:
        f.write(f"Accuracy: {correct/seen}")
    return correct/seen
def transformer_name(input):
    match = re.search(r'[^()/]+$', input)
    print(f"match = {match}")
    return match.group() if match else input
if __name__ =="__main__":
    results = []
    models = ["gemini-2.0-flash-exp", "gemini-1.5-flash", "gemini-2.0-flash-001",
              "gemini-2.0-flash-lite-preview-02-05", "gemini-1.5-pro", "claude-3-5-haiku-latest",
              "claude-3-5-sonnet-20241022", "grok-2-latest", "grok-2",
              "grok-beta", "grok-2-vision", "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B", "claude-3-7-sonnet-20250219"]
    for model in models:
        accuracy = run_experiment(grokexperiment(model=model, prompt_function=get_basic_prompt), ground_truth_csv_path='ground_truth.csv')
        results.append((model, accuracy))
    # Plotting the results
    plt.rcParams.update({'font.size': 5})
    model_names = [result[0] for result in results]
    accuracies = [result[1] for result in results]
    plt.figure(figsize=(11, 7))
    plt.bar(model_names, accuracies, color=['red', 'blue', 'yellow', "green", "purple", "orange", "pink", "brown", "cyan", "magenta"])
    plt.xlabel('Models', fontsize=7)
    plt.ylabel('Accuracy', fontsize=7)
    plt.xticks(rotation=60)
    plt.title(f'Accuracy of Different LLMs in Blocks Benchmark', fontsize=10)
    plt.ylim(0, 1)  # Assuming accuracy is between 0 and 1
    plt.show()

