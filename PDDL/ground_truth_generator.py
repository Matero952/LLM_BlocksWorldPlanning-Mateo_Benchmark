import subprocess
import pandas as pd
from PDDL.state_generator import generate_block_states
import json

"""
Module for the ground truth generator.
This module provides functions to generate PDDL (Planning Domain Definition Language) domain and problem files 
for a simple Blocksworld scenario, and to solve the generated PDDL problem using the Pyperplan solver. 
It also includes functionality to generate ground truth data for different block configurations.
Functions:
    generate_pddl(start_state, end_state):
        Generates a simple PDDL domain and problem to transition from start_state to end_state.

        Args:
            start_state (dict): A dictionary mapping block -> placement.
            end_state (dict): A dictionary mapping block -> placement with desired final configuration.
        Returns:
            tuple: (domain_pddl, problem_pddl)
    solve_pddl_plan(domain, problem):
        Solves the given PDDL problem using Pyperplan and returns the resulting plan or an error message.

        Args:
            domain (str): PDDL domain definition.
            problem (str): PDDL problem definition.
        Returns:
            dict: The resulting plan with 'pick' and 'place' actions or an error message.
    generate_ground_truth(blocks, save_dir):
        Generates ground truth data for different block configurations and saves it to a CSV file.

        Args:
            blocks (list): A list of block names.
            csv_path (str): path to save the ground truth csv to
        Returns:
            None
"""



def generate_pddl(start_state, end_state):
    """
    Generates a simple PDDL domain and problem to transition from start_state to end_state.

    Args:
        start_state (dict): A dictionary mapping block -> placement. 
                            For example: {'red': 'table', 'blue': 'red', ...}
        end_state (dict): A dictionary mapping block -> placement with desired final configuration.

    Returns:
        tuple: (domain_pddl, problem_pddl)
    """
    blocks = list(start_state.keys())

    # Define a standard Blocksworld domain in PDDL
    domain_pddl = """(define (domain blocksworld)
    (:requirements :strips)
    (:predicates
        (on ?x ?y)
        (ontable ?x)
        (clear ?x)
        (handempty)
        (holding ?x)
    )

    (:action pick-up
        :parameters (?x)
        :precondition (and (ontable ?x) (clear ?x) (handempty))
        :effect (and (holding ?x) (not (ontable ?x)) (not (clear ?x)) (not (handempty)))
    )

    (:action put-down
        :parameters (?x)
        :precondition (holding ?x)
        :effect (and (ontable ?x) (clear ?x) (handempty) (not (holding ?x)))
    )

    (:action stack
        :parameters (?x ?y)
        :precondition (and (holding ?x) (clear ?y))
        :effect (and (on ?x ?y) (clear ?x) (handempty) (not (holding ?x)) (not (clear ?y)))
    )

    (:action unstack
        :parameters (?x ?y)
        :precondition (and (on ?x ?y) (clear ?x) (handempty))
        :effect (and (holding ?x) (clear ?y) (not (on ?x ?y)) (not (clear ?x)) (not (handempty)))
    )
)
"""

    # Construct the initial state
    initial_state = []
    # If a block is 'table', it means it is on the table.
    # Otherwise, it is on another block.
    for block, placement in start_state.items():
        if placement == 'table':
            initial_state.append(f"(ontable {block})")
        else:
            initial_state.append(f"(on {block} {placement})")

    # Identify which blocks are clear
    # A block is clear if no other block is on top of it in the initial configuration
    blocks_above = set(start_state.values()) - {'table'}
    for block in blocks:
        if block not in blocks_above:
            # No block is on this block, so it is clear
            initial_state.append(f"(clear {block})")

    # The hand starts empty
    initial_state.append("(handempty)")

    # Construct the goal state
    goal_state = []
    for block, placement in end_state.items():
        if placement == 'table':
            goal_state.append(f"(ontable {block})")
        else:
            goal_state.append(f"(on {block} {placement})")

    problem_pddl = f"""
(define (problem blocksworld-problem)
    (:domain blocksworld)
    (:objects {" ".join(blocks)})
    (:init {" ".join(initial_state)})
    (:goal (and {" ".join(goal_state)}))
)
"""

    return domain_pddl, problem_pddl

def solve_pddl_plan(domain, problem):
    """
    Solves the given PDDL problem using Pyperplan.

    Args:
        domain (str): PDDL domain definition.
        problem (str): PDDL problem definition.

    Returns:
        str: The resulting plan or an error message.
    """
    # Save domain and problem to temporary files
    domain_file = "./domain.pddl"
    problem_file = "./problem.pddl"
    with open(domain_file, "w") as f:
        f.write(domain)
    with open(problem_file, "w") as f:
        f.write(problem)

    # Run Pyperplan solver
    solver_command = ["pyperplan", "--heuristic", "hff", "--search", "astar", domain_file, problem_file]
    
    result = subprocess.run(solver_command, capture_output=True, text=True)
    out_file = "./problem.pddl.soln"
    outputs = {"pick":"None", "place":"None"}
    with open(out_file, "r") as file:
        line1 = file.readline()
        line1 = line1.replace("(", "").replace(")", "").split(" ")
        assert line1[0] == "unstack" or line1[0] == "pick-up" or line1[0] == "", f"line1[0] not expected type instead was {line1[0]}"

        line2 = file.readline()
        line2 = line2.replace("(", "").replace(")", "").split(" ")
        assert line2[0] == "stack" or line2[0] == "put-down" or line2[0] == "", f"line2[0] not expected type instead was {line2[0]}"

        if line1[0] == "unstack" or line1[0] == "pick-up":
            outputs["pick"] = line1[1].strip()
        if line2[0] == "stack":
            outputs["place"] = line2[2].strip()
        if line2[0] == "put-down":
            outputs["place"] = "table"



        #print(f"{line1}")
        #print(f"{line2}")

    return outputs

        
def generate_ground_truth(blocks, csv_path):
    """
    Generates ground truth data for different block configurations and saves it to a CSV file.
    """
    starting_states = generate_block_states(blocks)
    ending_states = generate_block_states(blocks)
    df = pd.DataFrame(columns=['start_state', 'end_state', 'next_best_move'])

    for i, start_state in enumerate(starting_states):
        #print(f"State {i + 1}: {start_state}")

        for j, end_state in enumerate(ending_states):
            print(f"State {i + 1} {j+1}: \n{start_state=}\n{end_state=}")
            domain_pddl, problem_pddl = generate_pddl(start_state, end_state)
            best_move = solve_pddl_plan(domain_pddl, problem_pddl)
            print(f"   {best_move}")
            print()
            df.loc[len(df)] = [json.dumps(start_state), json.dumps(end_state), json.dumps(best_move)]
    df.to_csv(f"{csv_path}", index = False)
    return csv_path

if __name__ == "__main__":
    # Example start and end states:
    blocks = ["red_block", "blue_block", "yellow_block"]
    generate_ground_truth(blocks, "./ground_truth.csv")
