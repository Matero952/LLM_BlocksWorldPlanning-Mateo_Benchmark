from enum import Enum
class ComplexTestCases(Enum):
    #This contains more complex test cases of actual model outputs.
    TEST1 = ''''"{""red_block"": ""table"", ""blue_block"": ""table"", ""yellow_block"": ""table""}","{""red_block"": ""table"", ""blue_block"": ""table"", ""yellow_block"": ""table""}","{""pick"": ""None"", ""place"": ""None""}","{""pick"": ""None"", ""place"": ""None""}","Since the start state and the end state are identical (all blocks are already on the table), no move is necessary to reach the goal.

pick: None
place: None"
"{""red_block"": ""table"", ""blue_block"": ""table"", ""yellow_block"": ""table""}","{""red_block"": ""table"", ""blue_block"": ""table"", ""yellow_block"": ""red_block""}","{""pick"": ""yellow_block"", ""place"": ""red_block""}","{""pick"": ""yellow_block"", ""place"": ""red_block""}","I need to compare the start state and the end state to determine what actions are needed.

In the start state:
- red_block is on table
- blue_block is on table
- yellow_block is on table

In the end state:
- red_block is on table
- blue_block is on table
- yellow_block is on red_block

The difference is that yellow_block needs to be moved from the table to on top of red_block.

So the next best move is:

pick: yellow_block
place: red_block"'''
    TEST2 = '''"{""red_block"": ""table"", ""blue_block"": ""table"", ""yellow_block"": ""table""}","{""red_block"": ""table"", ""blue_block"": ""table"", ""yellow_block"": ""blue_block""}","{""pick"": ""yellow_block"", ""place"": ""blue_block""}","{""pick"": ""yellow_block"", ""place"": ""blue_block""}","I need to compare the start state and the desired end state to determine the best move.

In the start state, all blocks are on the table. In the end state, red and blue blocks should be on the table, but yellow_block should be on blue_block.

Since the yellow_block needs to move from the table to the blue_block, that's the move I should make:

pick: yellow_block
place: blue_block"
"{""red_block"": ""table"", ""blue_block"": ""table"", ""yellow_block"": ""table""}","{""red_block"": ""table"", ""blue_block"": ""red_block"", ""yellow_block"": ""table""}","{""pick"": ""blue_block"", ""place"": ""red_block""}","{""pick"": ""blue_block"", ""place"": ""red_block""}","Based on the start state and desired end state, I need to put the blue_block on top of the red_block while keeping the red_block and yellow_block on the table.

Looking at the start state, all blocks are on the table. In the end state, the only change is that blue_block should be on red_block.

Therefore, the next best move is:

pick: blue_block
place: red_block"'''
    TEST3 = ''''"{""red_block"": ""table"", ""blue_block"": ""table"", ""yellow_block"": ""table""}","{""red_block"": ""table"", ""blue_block"": ""red_block"", ""yellow_block"": ""blue_block""}","{""pick"": ""blue_block"", ""place"": ""red_block""}","{""pick"": ""blue_block"", ""place"": ""red_block""}","I need to determine the next best move to reach the desired configuration where yellow_block is on blue_block which is on red_block.

Looking at the start state, all blocks are on the table, and in the target state, we need to build a stack.

The best approach is to build this stack from the bottom up. Since red_block needs to be at the bottom of the stack, we should place blue_block on red_block first.

pick: blue_block
place: red_block"'''
    TEST4 = '''"{""red_block"": ""table"", ""blue_block"": ""table"", ""yellow_block"": ""table""}","{""red_block"": ""table"", ""blue_block"": ""yellow_block"", ""yellow_block"": ""table""}","{""pick"": ""blue_block"", ""place"": ""yellow_block""}","{""pick"": ""blue_block"", ""place"": ""yellow_block""}","I need to move the blocks to satisfy the desired end state where blue_block is on yellow_block, while both red_block and yellow_block remain on the table.

Looking at the start state, all blocks are on the table. To achieve the end state, I need to pick up the blue_block and place it on top of the yellow_block.

pick: blue_block
place: yellow_block"'''
    TEST5 = '''"{""red_block"": ""table"", ""blue_block"": ""table"", ""yellow_block"": ""red_block""}","{""red_block"": ""table"", ""blue_block"": ""table"", ""yellow_block"": ""red_block""}","{""pick"": ""None"", ""place"": ""None""}","{""pick"": ""None"", ""place"": ""None""}","The start state and the end state are identical. Both state that the red_block is on the table, the blue_block is on the table, and the yellow_block is on the red_block. Since we're already at the desired end state, no move is needed.

pick: None
place: None"'''