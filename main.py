from run_expiriment import run_experiment

"""
Runs a series of experiments to compare the performance of different language models on the
"""
if __name__ == "__main__":
    run_experiment("gpt-3.5-turbo-0125",  "basic_prompt")
    run_experiment("gpt-4o-mini",  "basic_prompt")
    run_experiment("gpt-4o-2024-11-20",  "basic_prompt")
    run_experiment("o1-preview-2024-09-12",  "basic_prompt")

