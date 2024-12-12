import json

def get_basic_prompt(start_state, end_state):
    # Construct the prompt for GPT-4
    prompt = f"""\nGiven the start state:\n"""
    for block, placement in start_state.items():
        prompt += f"{block} is on {placement}\n"
    prompt+="\n"
    prompt += """and desired end state:\n"""
    for block, placement in end_state.items():
        prompt += f"{block} is on {placement}\n"
    prompt+= "\n"
    prompt +="""what is the next best move to get us closer to the end state from the start state? Your answer needs to have two parts on two seperate lines.
    pick: object to be picked up
    place: object to put the picked object on

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
