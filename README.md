# Introduction to Artificial Intelligence - Programming Assignment 4

## Detailed installation instructions:

In order to run the code create a Python environment as follows: \
`Python3.10` \
`numpy==1.26.4`

And to run the project:
1. open the [main.py](src/main.py) script.
2. Update the `data_filepath` parameter with the path to the input txt file.
3. Run the `main` function.

## Explanation of the method employed in our algorithm

The reasoning algorithm is implemented using modified `Value Iteration` algorithm, with Bellman equation updates.\
At First, instead of setting arbitrary utility values for the states, 
we set the value of the goal state as `0` and the value of all the other states as `-np.inf`.\
Then, we iteratively update the utility value of each state using the Bellman equation until the values converge.

**Notice:** Firstly we update the utility of all the known states 
(where each edge in the states vector has a value from `['T','F']`), 
and then we update the unknown states
(where each states vector has an edge with `'U'` value).\
The value meaning:
- `'T'` - Blocked (True)
- `'F'` - Unblocked (False)
- `'U'` - Unknown

## How to work with the interface:
When you run the `main` function, you will be prompted with the following options:
```
Choose operation from the following options:
0. Print the value of each belief-state, and the optimal action in that belief state, if it exists.
1. Print the constructed policy.
2. Generate new graph instance.
3. Run simulator (Prerequisite: a graph instance must exists).
4. Quit.
Your choice: _
```

The available options are: `0`, `1`, `2`, `3`, `4`, where:
1. Option `0`: Prints the value of each belief-state in the following format:
   ```
   Vertex (0, 0):
     U['F']=-7.0, Optimal Action: Down
     U['T']=-7.0, Optimal Action: Down
     U['U']=-7.0, Optimal Action: Right
   
   Vertex (4, 3):
     U['F']=0.0, Optimal Action: no-op
     U['T']=0.0, Optimal Action: no-op
     U['U']=0.0, Optimal Action: no-op
   
   Vertex (0, 1):
      etc.
   ```
2. Option `1`: Prints the constructed policy in the following format:
   ```
   The constructed policy:
   -> Action: 'Right' (From '(0,0)' to '(0,1)')
   -> If (Blocked['(0,1) (0,2)']=F):
   ->-> Action: 'Down' (From '(0,1)' to '(1,1)')
   ->-> etc.
   ->-> Action: 'no-op', Path cost: -7 (Goal reached)
   -> If (Blocked['(0,1) (0,2)']=T):
   ->-> Action: 'Down' (From '(0,1)' to '(1,1)')
   ->-> etc.
   ->-> Action: 'no-op', Path cost: -7 (Goal reached)
   Policy Expected Utility: -7.0
   ```
3. Option `2`: Generates a new graph instance and prints the given state to each fragile edge in the following format:
   ```
   Generating new graph instance...
   Fragile edge: '(0,1) (0,2)' was set as: 'blocked'.
   Graph instance generated!
   
   Graph Instance State:
   #X 4 ; Maximum x coordinate: 4
   #Y 3 ; Maximum y coordinate: 3
   #P 3  A 0 ; Package 0: delivered, By agent 0
   
   #E 0 ; Edge 0: always blocked
   #E 0 ; Edge 1: always blocked
   #E 0 ; Edge 2: always blocked
   #A 0  L 0 0  A 0  S 0 ; Agent 0: Normal agent, Location: (0 0), Number of actions: 0, Score: 0

   #T 0.0 ; Total Time unit passed: 0.0
   ```
4. Option `3`: Runs simulator on the last created graph instance and report the steps the agent performed 
   in the same format as we submitted on assignment 1:
   ```
   # Clock Time 0.0:
   Agent 0 (Normal) Action: Right
   # Clock Time 1.0:
   etc.
    
   # Clock Time 7.0:
   Goal achieved: All available packages have been delivered or disappeared
   Final State:
   #X 4 ; Maximum x coordinate: 4
   #Y 3 ; Maximum y coordinate: 3
   #P 3  A 0 ; Package 0: delivered, By agent 0
   
   #E 0 ; Edge 0: always blocked
   #E 0 ; Edge 1: always blocked
   #E 0 ; Edge 2: always blocked
   #A 0  L 4 3  A 7  S 1 ; Agent 0: Normal agent, Location: (4 3), Number of actions: 7, Score: 1

   #T 7.0 ; Total Time unit passed: 7.0
   ```
5. Option `4`: Quits the program.

## Non-trivial example runs on at least 2 scenarios, including the input and output:

See the file [input_results.txt](input_results.txt) for the example runs of the 2 scenarios 
in the following input files:
- [input1.txt](input%2Finput1.txt)
- [input2.txt](input%2Finput2.txt)