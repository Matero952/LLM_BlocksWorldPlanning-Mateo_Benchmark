from prompts import get_basic_prompt

import pandas as pd
from experiments import OAI_Experiment
import json
import os

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

    
def run_experiment(experiment, suffix=""):
    """
    Runs the experiment with the given model and prompt function, processes each sample in the dataset, 
    and saves the results to a CSV file.

    Args:
        experiment (OAI_Experiment): An instance of the OAI_Experiment class, which includes the model and prompt function to be used.
        suffix (str, optional): A suffix to be added to the results directory and file names. Defaults to "".

    Returns:
        None
    """

    print(f"\n\n\n\nbegining to run experiment {experiment.model_name=} {experiment.prompt_function=}")
    df = pd.read_csv('./ground_truth.csv')

    os.makedirs("./results/", exist_ok=True)
    save_dir = os.path.join("./results/", f'{experiment.model_name}{suffix}/')
    os.makedirs(save_dir, exist_ok=True)

    new_df = pd.DataFrame(columns=['start_state', 'end_state', 'next_best_move', 'predicted_next_best_move', "response"])
    newdf_path = os.path.join(save_dir, f'{experiment.model_name}{suffix}_results.csv')

    correct = 0
    seen = 0
    for index, row in df.iterrows():
        start_state = json.loads(row['start_state'])
        end_state = json.loads(row['end_state'])
        label = json.loads(row['next_best_move'])
        response, pred = experiment.process_sample(start_state, end_state)
        correct += 1 if pred == label else 0
        seen += 1
        new_df.loc[len(new_df)] = [json.dumps(start_state), json.dumps(end_state), json.dumps(label), json.dumps(pred), response]
        print(f"\rProcessing: {index+1}/{len(df)}, accuracy:{correct/seen} ({correct} / {seen})" , end="")
        new_df.to_csv(newdf_path, index = False)


if __name__ =="__main__":
    models = "gpt-4o-mini"
    run_experiment(OAI_Experiment(models, get_basic_prompt))