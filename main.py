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
    quotas = [5.1, 4.1, 30.1]
    #Quota limits for my time.sleep()
    models = ["gemini-2.0-flash-001", "gemini-2.0-flash-lite-preview-02-05"]#"gemini-2.0-flash-exp", "gemini-1.5-flash", "gemini-1.5-pro", ]
    # mapped_models = list(zip(models, quotas))
    # print(f"Mapped models: {mapped_models}")
    #NOTES ON QUOTA:
    #Gemini 1.5 pro has very low quota
    # gpt_models = ["gpt-3.5-turbo-0125", "gpt-4o-mini", "gpt-4o-2024-11-20"] #, "o1-preview-2024-09-12"]
    results = []
    # for gpt_model in gpt_models:
    for model in models:
        if model == "gemini-2.0-flash-exp":
            model_quota = 5.1
        elif model == "gemini-1.5-flash":
            model_quota = 4.1
        else:
            model_quota = 35
        accuracy = run_expiriment.run_experiment(GEMExperiment(model, get_basic_prompt), ground_truth_csv_path=csv_path, quota=model_quota)
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
    #TODO Create another figure comparing the results of all of the models.

