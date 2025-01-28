import re
from openai import OpenAI
from APIKeys import OAI_APIKEY

"""
This module defines an Experiment class to interact with a language model API for processing samples
and extracting specific actions from the model's response. It includes functionality to run experiments
with different models and compare the predictions with ground truth labels.
Classes:
    Experiment: A class to handle the interaction with the language model API and process samples.
Functions:
    main: The entry point of the script, which sets up the experiments and runs them with different models.
Usage:
    Run this script as a standalone module to execute the experiments and compare the model predictions
    with the ground truth labels.
Example:
    $ python experiment.py
Dependencies:
    - re
    - pandas
    - json
    - openai
    - prompts (local module)
    - APIKeys (local module)
"""


class OAI_Experiment:
    """
    A class to represent an experiment using OpenAI's API for generating responses based on given prompts.
    Attributes:
    ----------
    model_name : str
        The name of the model to be used for generating responses.
    prompt_function : function
        A function that generates a prompt string based on the start and end states.
    client : OpenAI
        An instance of the OpenAI client initialized with the provided API key.
    Methods:
    -------
    __init__(self, model_name, prompt_function):
        Initializes the OAI_Experiment with the specified model name and prompt function.
    process_sample(self, start_state, end_state):
        Generates a prompt using the prompt function, sends it to the OpenAI API, and processes the response.
        Parameters:
        ----------
        start_state : any
            The initial state to be used in the prompt.
        end_state : any
            The desired end state to be used in the prompt.
        Returns:
        -------
        result : str
            The raw response content from the OpenAI API.
        output : dict
            A dictionary containing the extracted 'pick' and 'place' instructions from the response.
    """

    def __init__(self, model_name, prompt_function):
        self.model_name = model_name
        self.prompt_function = prompt_function
        self.client = OpenAI(api_key= OAI_APIKEY)

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

    

    model = "gpt-4o-mini"
    print(model)
    experiment_4o = OAI_Experiment(model, get_basic_prompt)
    df = pd.read_csv('./ground_truth.csv')

    row = df.sample(n=1).iloc[0]
    start_state = json.loads(row['start_state'])
    end_state = json.loads(row['end_state'])
    label = json.loads(row['next_best_move'])
    result, pred = experiment_4o.process_sample(start_state, end_state)
    print(f"{start_state=}")
    print(f"{end_state=}")
    print(f"{pred=}")
    print(f"{label=}")
    print(f"{result=}")
    print(f"{pred==label}")


