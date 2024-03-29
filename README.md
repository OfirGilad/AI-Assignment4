# Introduction to Artificial Intelligence - Programming Assignment 4

## Detailed installation instructions:

In order to run the code create a Python environment as follows: \
`Python3.10` \
`numpy==1.26.3`

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
1. Generate new graph instance.
2. Run simulator (Prerequisite: a graph instance must exists).
3. Quit.
Your choice: _
```

The available options are: `0`, `1`, `2`, `3`, where:
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
2. Option `1`: Generates a new graph instance and prints the given state to each fragile edge in the following format:
   ```
   Generating new graph instance...
   Fragile edge: '(0,1) (0,2)' was set as 'blocked'.
   Graph instance generated!
   ```
3. Option `2`: Runs simulator on the last created graph instance and report the steps the agent performed 
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
4. Option `3`: Quits the program.