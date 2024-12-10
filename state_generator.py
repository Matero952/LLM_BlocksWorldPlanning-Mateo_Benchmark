from itertools import product
import subprocess
import pandas as pd
def generate_block_states(blocks):
    """
    Generates all possible states for a list of blocks, where each block can be
    placed either on the table or on top of another block, with the constraint that
    no two blocks can be on the same block simultaneously.

    Args:
        blocks (list): List of block identifiers (e.g., ['A', 'B', 'C']).

    Returns:
        list: A list of dictionaries representing all possible states.
    """
    states = []

    # Generate all possible placements: table or other blocks
    possible_placements = ['table'] + blocks

    # Generate all combinations of placements for each block
    all_combinations = product(possible_placements, repeat=len(blocks))

    for combination in all_combinations:
        state = {}
        valid = True
        table_support = set()

        for block, placement in zip(blocks, combination):
            # A block cannot be placed on itself
            if placement == block:
                valid = False
                break
            state[block] = placement
            if placement == 'table':
                table_support.add(block)

        if not valid:
            continue

        # Check that no two blocks are on the same non-table block
        # Extract all placements that are blocks (not 'table')
        non_table_placements = [p for p in state.values() if p != 'table']
        if len(non_table_placements) != len(set(non_table_placements)):
            # This means there's a duplicate placement, so at least two blocks
            # are on the same block
            valid = False

        if not valid:
            continue

        # Check for cycles and ensure at least one block is on the table
        if valid and table_support:
            for block in blocks:
                current = block
                visited = set()
                while current != 'table':
                    if current in visited or current not in state:
                        valid = False
                        break
                    visited.add(current)
                    current = state[current]
                if not valid:
                    break

        if valid and table_support:
            states.append(state)

    return states
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
    outputs = {"pick":None, "place":None}
    with open(out_file, "r") as file:
        line1 = file.readline()
        line1 = line1.replace("(", "").replace(")", "").split(" ")
        assert line1[0] == "unstack" or line1[0] == "pick-up" or line1[0] == "", f"line1[0] not expected type instead was {line1[0]}"

        line2 = file.readline()
        line2 = line2.replace("(", "").replace(")", "").split(" ")
        assert line2[0] == "stack" or line2[0] == "put-down" or line2[0] == "", f"line2[0] not expected type instead was {line2[0]}"

        if line1[0] == "unstack" or line1[0] == "pick-up":
            outputs["pick"] = line1[1]
        if line2[0] == "stack":
            outputs["place"] = line2[2]
        if line2[0] == "put-down":
            outputs["place"] = "table"



        #print(f"{line1}")
        #print(f"{line2}")

        

    return outputs
    

# Example usage
if __name__ == "__main__":
    # Example start and end states:
    blocks = ["red_block", "blue_block", "yellow_block"]
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
            df.loc[len(df)] = [start_state, end_state, best_move]
    df.to_csv("blox_world.csv", index = False)

