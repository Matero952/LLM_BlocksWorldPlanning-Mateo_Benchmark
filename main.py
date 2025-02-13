from Experiments.Gemini.GEMExperiment import GEMExperiment
from ground_truth_generator import generate_ground_truth
from prompts import get_basic_prompt
from matplotlib import pyplot as plt
import run_expiriment
"""
Runs a series of experiments to compare the performance of different language models on the
"""
if __name__ == "__main__":
    blocks = ['red_block', 'blue_block', 'yellow_block']
    csv_path = generate_ground_truth(blocks, "ground_truth.csv")
    models = ["gemini-2.0-flash-exp", "gemini-1.5-flash", "gemini-2.0-flash-001",
              "gemini-2.0-flash-lite-preview-02-05"]

    results = []
    # for gpt_model in gpt_models:
    for model in models:
        accuracy = run_expiriment.run_experiment(GEMExperiment(model, get_basic_prompt), ground_truth_csv_path=csv_path)
        results.append((model, accuracy))
    # Plotting the results
    model_names = [result[0] for result in results]
    accuracies = [result[1] for result in results]

    plt.figure(figsize=(10, 6))
    plt.bar(model_names, accuracies, color=['red', 'blue', 'yellow'])
    plt.xlabel('Gemini Models')
    plt.ylabel('Accuracy')
    plt.title('Accuracy of Different GPT Models')
    plt.ylim(0, 1)  # Assuming accuracy is between 0 and 1
    plt.show()

