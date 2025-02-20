from Experiments.Gemini.GEMExperiment import GEMExperiment
from prompts import get_basic_prompt
import pandas as pd
import json
import os
import time
import matplotlib.pyplot as plt
from Experiments.Claude.ClaudeExperiment import ClaudeExperiment


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
    quotas = {"gemini-2.0-flash-exp": 5.01, "gemini-1.5-flash": 4.01, "gemini-2.0-flash-001": 4.01,
              "gemini-2.0-flash-lite-preview-02-05": 4.01, "gemini-1.5-pro": 33, "claude-3-5-haiku-latest" : 0}
    if experiment.model_name not in quotas.keys():
        print(f"Error: {experiment.model_name} is not a valid model name.")
    print(f"Experiment name: {experiment.model_name}")
    print(f"\n\n\n\nbeginning to run experiment {experiment.model_name=} {experiment.prompt_func=}")
    df = pd.read_csv(ground_truth_csv_path)
    os.makedirs("./results/", exist_ok=True)
    save_dir = os.path.join("./results/", f'{experiment.model_name}{suffix}/')
    os.makedirs(save_dir, exist_ok=True)
    newdf_path = os.path.join(save_dir, f'{experiment.model_name}{suffix}_results.csv')
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
    with open(os.path.join(save_dir, f'{experiment.model_name}{suffix}_accuracy.txt'), 'w') as f:
        f.write(f"Accuracy: {correct/seen}")
    return correct/seen

if __name__ =="__main__":
    results = []
    models = ["claude-3-5-haiku-latest"]
    for model in models:
        accuracy = run_experiment(ClaudeExperiment(model, get_basic_prompt), ground_truth_csv_path="ground_truth.csv")
        results.append((model, accuracy))
    # Plotting the results
    plt.rcParams.update({'font.size': 5})
    model_names = [result[0] for result in results]
    accuracies = [result[1] for result in results]
    plt.figure(figsize=(10, 6))
    plt.bar(model_names, accuracies, color=['red', 'blue', 'yellow', "green", "purple"])
    plt.xlabel('Claude Test', fontsize=10)
    plt.ylabel('Accuracy', fontsize=10)
    plt.title(f'Accuracy of {model}', fontsize=15)
    plt.ylim(0, 1)  # Assuming accuracy is between 0 and 1
    plt.show()

