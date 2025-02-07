import main
from Experiments.Gemini.GEMExperiment import GEMExperiment
from prompts import get_basic_prompt
import pandas as pd
import json
import os
import re
import time

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

    
def run_experiment(experiment, ground_truth_csv_path, quota, suffix=""):
    """
    Runs the experiment with the given model and prompt function, processes each sample in the dataset, 
    and saves the results to a CSV file.

    Args:
        experiment (OAI_Experiment): An instance of the OAI_Experiment class, which includes the model and prompt function to be used.
        suffix (str, optional): A suffix to be added to the results directory and file names. Defaults to "".

    Returns:
        accuracy: float
    """

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
    # new_df = pd.DataFrame(columns=['start_state', 'end_state', 'next_best_move', 'predicted_next_best_move', "response"])
    # newdf_path = os.path.join(save_dir, f'{experiment.model_name}{suffix}_results.csv')
    correct = 0
    seen = 0
    for index, row in df.iterrows():
        response, pred = None, None
        match = False
        start_state = json.loads(row['start_state'])
        end_state = json.loads(row['end_state'])
        label = json.loads(row['next_best_move'])
        # assert index < len(df), "Please work"
        if (index < len(new_df) and
                new_df.loc[index, 'start_state'] == json.dumps(start_state) and
                new_df.loc[index, 'end_state'] == json.dumps(end_state)):
            if new_df.loc[index, 'predicted_next_best_move'] == json.dumps(label):
                print("Checking")
                match = True
                if match:
                    correct += 1
                    seen += 1
                else:
                    seen += 1
        else:
            response, pred = experiment.process_sample(start_state, end_state)
            print("Processing")
            correct += 1 if pred == label else 0
            seen += 1
            new_df = pd.concat([new_df, pd.DataFrame(
                [[json.dumps(start_state), json.dumps(end_state), json.dumps(label), json.dumps(pred), response]],
                columns=['start_state', 'end_state', 'next_best_move', 'predicted_next_best_move', "response"])],
                               ignore_index=True)

        # new_df.loc[len(new_df)] = [json.dumps(start_state), json.dumps(end_state), json.dumps(label), json.dumps(pred), response]
        print(f"\rProcessing: {index + 1}/{len(df)}, accuracy:{correct / seen} ({correct} / {seen})", end="")
        new_df.to_csv(newdf_path, index=False)
        time.sleep(quota)
    with open(os.path.join(save_dir, f'{experiment.model_name}{suffix}_accuracy.txt'), 'w') as f:
        f.write(f"Accuracy: {correct/seen}")
    return correct/seen

if __name__ =="__main__":
    models = "gemini-2.0-flash-exp"
    run_experiment(GEMExperiment(models, get_basic_prompt), ground_truth_csv_path="ground_truth.csv", quota=5.1)

