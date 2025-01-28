from run_expiriment import run_experiment
from ground_truth_generator import generate_ground_truth
from prompts import get_basic_prompt
from experiments import OAI_Experiment
from matplotlib import pyplot as plt
"""
Runs a series of experiments to compare the performance of different language models on the
"""
if __name__ == "__main__":
    blocks = ['red_block', 'blue_block', 'yellow_block']
    csv_path = generate_ground_truth(blocks, "./ground_truth.csv")
    gpt_models = ["gpt-3.5-turbo-0125", "gpt-4o-mini", "gpt-4o-2024-11-20"] #, "o1-preview-2024-09-12"]

    results = []
    for gpt_model in gpt_models:
        accuracy = run_experiment(OAI_Experiment(gpt_model, get_basic_prompt), ground_truth_csv_path=csv_path)
        results.append((gpt_model, accuracy))
    # Plotting the results
    model_names = [result[0] for result in results]
    accuracies = [result[1] for result in results]

    plt.figure(figsize=(10, 6))
    plt.bar(model_names, accuracies, color=['red', 'blue', 'yellow'])
    plt.xlabel('GPT Models')
    plt.ylabel('Accuracy')
    plt.title('Accuracy of Different GPT Models')
    plt.ylim(0, 1)  # Assuming accuracy is between 0 and 1
    plt.show()

