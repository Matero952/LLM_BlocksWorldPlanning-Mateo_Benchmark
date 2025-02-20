import re
import json
from dotenv import load_dotenv
import pandas as pd
load_dotenv()
dotenv_path = '/home/mateo/Github/LLM_Blocks-Mateo/.env'
load_dotenv(dotenv_path)
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from huggingface_hub import login
login()

class transform:
    def __init__(self, model, prompt_func):
        self.model = AutoModelForSequenceClassification.from_pretrained(model)
        self.prompt_func = prompt_func
        self.tokenizer = AutoTokenizer.from_pretrained(model)
    def process_sample(self, start, end):
        prompt = self.prompt_func(start, end)
        inputs = self.tokenizer(prompt, return_tensors="pt").to('cuda')
        outputs = self.model(**inputs)
        result = (self.tokenizer.decode(outputs[0], skip_special_tokens=True))
        pick_match = re.search(r"(?i)pick\s*:\s*(.*)", result)
        place_match = re.search(r"(?i)place\s*:\s*(.*)", result)
        pick_str = pick_match.group(1).strip()
        place_str = place_match.group(1).strip()
        output = {"pick": pick_str, "place": place_str}
        return result, output
if __name__ == "__main__":
    from prompts import get_basic_prompt
    print(f"Beginning experiment")
    model= "meta-llama/Meta-Llama-3-8B"
    experiment = transform(model, get_basic_prompt)
    df = pd.read_csv('../../ground_truth.csv')
    row = df.sample(n=1).iloc[0]
    start_state = json.loads(row['start_state'])
    end_state = json.loads(row['end_state'])
    label = json.loads(row['next_best_move'])
    result, pred = experiment.process_sample(start_state, end_state)
    print(f"Result: {result}, Prediction: {pred}")


