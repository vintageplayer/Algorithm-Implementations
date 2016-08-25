# Author : Aditya Agarwal
# Program to convert an epsilon NFA to a DFA

import sys

symbol_transition		= {}
epsilon_closures		= {}
number_of_states		= 0
DFA 					= {}
DFA_states_list			= []
DFA_number_of_states	= 0

def check_requirements():

	if len(sys.argv)!=2:
		print('Invalid number of arguments...')
		sys.exit(1)

	option = int(sys.argv[1])

	if option != 0 and option != 1 :

		print('Usage Error!!')
		print('0 - Interactive Mode')
		print('1 - File Input Mode')
		sys.exit(1)

	return option


def get_state_map(transitions):

	symbol_transition['a'] = {}
	symbol_transition['b'] = {}
	symbol_transition['e'] = {}

	for trainsition in transitions:
		parts	 = trainsition.split(',')
		parts[0] = int(parts[0])
		parts[1] = int(parts[1])

		if symbol_transition[parts[2]].get(parts[0]):
			symbol_transition[parts[2]][parts[0]].append(parts[1])
		else:
			symbol_transition[parts[2]][parts[0]]	 = [parts[1]]


def calculate_epsilon_closure():
	for i in range(0,number_of_states):
		temp 	= []
		not_visited = [i]

		while len(not_visited)>0 :
			curr_symbol = not_visited.pop()
			temp.append(curr_symbol)
			if symbol_transition['e'].get(curr_symbol):
				for state in symbol_transition['e'][curr_symbol]:
					if state not in temp :
						if state not in not_visited :
							not_visited.append(state)

		epsilon_closures[i] = set(temp)

def get_a_transition_states(astate):
	
	result	= []

	test_result = []
	temp = []
	flag	= 0

	for state in DFA[astate]['states']:
		if symbol_transition['a'].get(state):
			flag = 1
			for end_point in symbol_transition['a'][state]:
				for reachable_state in epsilon_closures[end_point]:
					test_result.append(reachable_state)

	if flag == 0 :
		return None

	return set(test_result)

def get_b_transition_states(astate):
	
	result	= []
	flag	= 0

	for state in DFA[astate]['states']:
		if symbol_transition['b'].get(state):
			flag = 1
			for end_point in symbol_transition['b'][state]:
				for reachable_state in epsilon_closures[end_point]:
					result.append(reachable_state)

	if flag == 0 :
		return None

	return set(result)


def complete_DFA():
	global DFA_number_of_states

	unmapped_states = [0]
	while len(unmapped_states)>0:

		state = unmapped_states.pop()

		end_state = get_a_transition_states(state)
		DFA[state]['a'] = end_state

		if end_state != None :
			if end_state not in DFA_states_list:
				DFA_number_of_states			   += 1
				unmapped_states.append(DFA_number_of_states)
				DFA[DFA_number_of_states]			= {}
				DFA[DFA_number_of_states]['states'] = end_state
				DFA_states_list.append(end_state)

		end_state = get_b_transition_states(state)
		DFA[state]['b'] = end_state

		if end_state != None :
			if end_state not in DFA_states_list:
				DFA_number_of_states			   += 1
				unmapped_states.append(DFA_number_of_states)
				DFA[DFA_number_of_states]			= {}
				DFA[DFA_number_of_states]['states'] = end_state
				DFA_states_list.append(end_state)

def get_dfa(transitions):

	get_state_map(transitions)

	print('The transitions found on each symbol are as follows :')
	# print(symbol_transition)
	for i in range(0,number_of_states):
		if symbol_transition['a'].get(i):
			for end_point in symbol_transition['a'][i]:
				print(str(i)+' --a--> '+str(end_point))
		if symbol_transition['b'].get(i):
			for end_point in symbol_transition['b'][i]:
				print(str(i)+' --b--> '+str(end_point))
		if symbol_transition['e'].get(i):
			for end_point in symbol_transition['e'][i]:
				print(str(i)+' --e--> '+str(end_point))

	calculate_epsilon_closure()

	print('\nThe epsilon closure for each state is as follows :')
	for i in range(0,number_of_states):
		string = '{'
		for reachable_state in epsilon_closures[i]:
			string+=str(reachable_state)+','

		string = string[:-1]
		string += '}'
		print(str(i)+' = '+string)

	DFA[0] = {}
	DFA[0]['states'] = epsilon_closures[0]
	DFA_states_list.append(epsilon_closures[0])

	complete_DFA()

	print('\nObtained DFA is as follows :')
	print(DFA)
	print('States of the DFA : ')
	base_value = 65
	for i in range(0,DFA_number_of_states+1):
		string = ' = {'
		for element in DFA[i]['states']:
			string += str(element) + ','
		string = string[:-1]
		print(chr(base_value+i)+string+'}')

	print('\nThe transitions on each state are as follows :')
	for i in range(0,DFA_number_of_states+1):
		if DFA[i]['a'] != None:
			for j in range(0,DFA_number_of_states+1):
				if DFA[i]['a'] == DFA[j]['states']:
					print(chr(base_value+i)+' --a--> '+chr(base_value+j))

		if DFA[i]['b'] != None:
			for j in range(0,DFA_number_of_states+1):
				if DFA[i]['b'] == DFA[j]['states']:
					print(chr(base_value+i)+' --b--> '+chr(base_value+j))

	print('\nStart state of the DFA is : A')
	last_nfa_state = number_of_states - 1
	string = ' = {'
	for i in range(0,DFA_number_of_states+1):
		if last_nfa_state in DFA[i]['states']:
			string+=chr(base_value+i)+','
	string = string[:-1]
	print('Set of final states are as follows : '+string+'}')
# Start of the program

option = check_requirements()

if option == 1:
	try:
		input_file = open('../data/eNFA.txt','r').read()
	except FileNotFoundError:
		print('ERROR!! Input file is not present!!')
		sys.exit(1)

	transitions = input_file.split('\n')
	number_of_states = int(transitions.pop(0))
	get_dfa(transitions)

else:
	print('Enter number of states : ')
	print('Enter number of transitions : ')