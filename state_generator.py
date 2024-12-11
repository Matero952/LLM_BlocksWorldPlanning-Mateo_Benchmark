from itertools import product

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


if __name__ == "__main__":
    blocks = ["red_block", "blue_block", "yellow_block"]
    states = generate_block_states(blocks)
    for i, state in enumerate(states):
            print(f"State {i + 1}: {state=}\n")
