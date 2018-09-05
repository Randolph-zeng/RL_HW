import argparse
import json
import mdptoolbox
import numpy as np


def get_reward_matrix(isBadSide, prev_vals, N):
	pass


def get_prob_matrix(isBadSide, N):
	'''
	Args:
		isBadSide: array indicating which side is ending side (with value 1) 
		N: number of sides in the dice
	Return:
		probs: matrix with shape (A, S, S). In our setting A = {roll, quit}
		and S = {0, 1, 2, 3 .... N, N+1, N+2} where 0 stand for the initial 
		start state and N+1 and N+2 stand for winning and losing state 
	'''
	probs = np.zeros((2, N+3, N+3))
	for action in range(2):
		for state_curr in range(N+3):
			# For initial state
			if state_curr == 0:
				if action == 0:
					for stage_iter in range(1, N+1):
						probs[action,state_curr,stage_iter] = 1/N
				else:
					probs[action,state_curr,-2] = 1
				continue
			# Winning state stay in winning state forever
			if state_curr == N+1:
				probs[action,state_curr,-2] = 1
				continue
			# Losing state stay in losing state forever
			if state_curr == N+2:
				probs[action,state_curr,-1] = 1
				continue
			# For state from 1 to N
			if action == 0:
				# prob for action roll, note possibility for state 0 is always zero
				if isBadSide[state_curr-1] == 0:
					for stage_iter in range(1, N+1):
						probs[action,state_curr,stage_iter] = 1/N
				else:
					# N+2 is the losing state, roll on ending state goes to losing state
					probs[action,state_curr,-1] = 1
			else:
				# prob for action quit
				if isBadSide[state_curr-1] == 0:
					# N+1 is the winning state, quit on non-ending state goes to winning state
					probs[action,state_curr,-2] = 1
				else:
					# N+2 is the losing state, quit on ending state goes to losing state
					probs[action,state_curr,-1] = 1
	return probs


def get_optimal_val_diff(prev_vals, curr_vals):
	return sum(abs(curr_vals - prev_vals))


def main():
    # load mdp info
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', "--mdp_info", required=True, 
    	help="The path to the file that contains MDP problem info ", type= str)
    parser.add_argument('-s', "--res_path", required=True, 
    	help="The path to the file that stores the result ", type= str)
    args = parser.parse_args()
    with open(args.mdp_info,"r") as file:
    	mdp_info = json.load(file)

    # convergence condition 
    threshold = 0.001 
    res = {}
    # Set up params for value iteration 
    for idx,problem_info in enumerate(mdp_info["problems"]):
    	num_sides = problem_info["N"]
    	isBadSide = problem_info["isBadSide"]
    	# Get mdp variables
    	prev_vals = np.zeros(num_sides)
    	curr_vals = np.ones(num_sides)
    	# This is consistent throughout iterations
    	probs = get_prob_matrix(num_sides) 
    	while get_optimal_val_diff(prev_vals, curr_vals) > threshold:
    		# update reward function
    		rewards = get_reward_matrix(prev_vals, num_sides)
    		# run the value iteration
    		value_iter = mdptoolbox.mdp.ValueIteration(probs, rewards, 1)
			value_iter.run()
			prev_vals = curr_vals
			curr_vals = np.array(list(value_iter.V))
		# store results
    	res[idx] = curr_vals

    # dump to file
    with open(args.res_path,"r") as file:
    	json.dump(file,res)


if __name__ == '__main__':
	main()