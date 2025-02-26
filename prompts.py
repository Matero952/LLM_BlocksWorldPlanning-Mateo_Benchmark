"""
    This module contains functions to generate prompts for block stacking tasks for language models (LLMs).

    Functions:
        get_basic_prompt(start_state, end_state):
            Constructs a string prompt for an LLM to determine the next best move 
"""
def get_basic_prompt(start_state, end_state):
    """
    Constructs a string prompt for a language model (LLM) to determine the next best move 
    to transition from the start state to the end state in a block world scenario.

    Args:
        start_state (dict): A dictionary representing the initial positions of blocks. 
                            Keys are block names, and values are their placements.
        end_state (dict): A dictionary representing the desired final positions of blocks. 
                          Keys are block names, and values are their placements.

    Returns:
        str: A formatted string prompt describing the start state, the desired end state, 
             and a request for the next best move to transition from the start state to the end state.
    """
    # Construct string prompt for an LLM
    prompt = f"""\nGiven the start state:\n"""
    for block, placement in start_state.items():
        prompt += f"   {block} is on {placement}\n"
    prompt+="\n"
    prompt += """and desired end state:\n"""
    for block, placement in end_state.items():
        prompt += f"   {block} is on {placement}\n"
    prompt+= "\n"
    prompt +="""what is the next best move to get us closer to the end state from the start state? Your answer needs to have two parts on two seperate lines, and also only one pick and place and please make sure to have the pick and place.
   pick: *object to be picked up*
   place: *object to put the picked object on*

if there is no block to move please have
   pick: None
   place: None
    """
    return prompt

# Example usage
if __name__ == "__main__":
    start_state = {'red_block': 'yellow_block', 'blue_block': 'red_block', 'yellow_block': 'table'}
    end_state = {'red_block': 'blue_block', 'blue_block': 'yellow_block', 'yellow_block': 'table'}
    prompt = get_basic_prompt(start_state, end_state)
    print(prompt)
