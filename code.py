# Here is an exmaple input to test your code on. It is solveable.
# nodes = 'CHTPS'
# arcs = [(0,1), (0,2), (1,2), (1,3), (1,4), (2,3), (2,4)]
# max_steps = 1000
# solve_csp(nodes, arcs, max_steps)

# "- Triangle - The leftmost digit of the product of all of its neightbors\n",
# "- Square - The rightmost digit of of the product of all its neighbors\n",
# "- Hexagon - The leftmost digit of the sum of all its neighbors\n",
# "- Pentagon - The rightmost digit of the sum of all its neighbors\n",
# "- Circle - No contraints\n"
import random
from random import choice

def getStartState(nodes):
	node_values = []
	for i in range(len(nodes)):
		node_values.append(random.randint(1, 9))
	return node_values

def isConflict(node, i, node_values, node_neigh):
	if node == 'T':
		total = 1
		for j in range(len(node_neigh[i])):
			total *= node_values[node_neigh[i][j]]
		#find leftmost digit
		left, total = total, total // 10
		while total:
			left = left // 10
			total = total // 10
		if left != node_values[i]:
			return True
	elif node == 'S':
		total = 1
		for j in range(len(node_neigh[i])):
			total *= node_values[node_neigh[i][j]]
		if total % 10 != node_values[i]:
			return True
	elif node == 'P':
		total = 0
		for j in range(len(node_neigh[i])):
			total += node_values[node_neigh[i][j]]
		if total % 10 != node_values[i]:
			return True
	elif node == 'H':
		total = 1
		for j in range(len(node_neigh[i])):
			total += node_values[node_neigh[i][j]]
		#find leftmost digit
		left, total = total, total // 10
		while total:
			left = left // 10
			total = total // 10
		if left != node_values[i]:
			return True

	return False

def getVar(nodes, node_values, arcs, node_neigh):
	#find all the conflict node and random choose one from it. 
	node_conflict = []
	for i in range(len(nodes)):
		if nodes[i] == 'C':
			node_conflict.append(i)
			continue
		if (isConflict(nodes[i], i, node_values, node_neigh)):
			node_conflict.append(i)

	if len(node_conflict) == 1:
		return -1
	else:
		return choice(node_conflict)

def count_conflict(nodes, node_values, node_neigh):
	#count how many conflicts in the node_values
	count_conflict = 0
	for i in range(len(node_values)):
		if isConflict(nodes[i], i, node_values, node_neigh):
			count_conflict += 1

	return count_conflict

def getValue(nodes, node_values, pos, node_neigh):
	#get a value with a smaller conflicts
	curr_conflict = count_conflict(nodes, node_values, node_neigh)
	curr_val = node_values[pos]

	for i in range(1, 10):
		if i == curr_val:
			continue
		node_values[pos] = i
		temp_count = count_conflict(nodes, node_values, node_neigh)
		if temp_count <= curr_conflict:
			curr_conflict = temp_count
			curr_val = i

	node_values[pos] = curr_val
	return curr_val

def solve_csp(nodes, arcs, max_steps):
	"""
	This function solves the csp using the MinConflicts Search
	Algorithm.

	INPUTS:
	nodes:      a list of letters that indicates what type of node it is,
	            the index of the node in the list indicates its id
	            letters = {C, T, S, P, H}
	arcs:       a list of tuples that contains two numbers, indicating the 
	            IDS of the nodes the arc connects. 
	max_steps:  max number of steps to make before giving up

	RETURNS: a list of values for the soltiion to the CSP where the 
	         index of the value correxponds the the value for that
	         given node.
	"""

	# YOUR CODE HERE
	node_values = getStartState(nodes)
	#construct the neighbour of each node
	node_neigh = {}
	for i in range(len(arcs)):
		if arcs[i][0] not in node_neigh:
			node_neigh.setdefault(arcs[i][0], []).append(arcs[i][1])
		else:
			if arcs[i][1] not in node_neigh[arcs[i][0]]:
				node_neigh[arcs[i][0]].append(arcs[i][1])
		if arcs[i][1] not in node_neigh:
			node_neigh.setdefault(arcs[i][1], []).append(arcs[i][0])
		else:
			if arcs[i][0] not in node_neigh[arcs[i][1]]:
				node_neigh[arcs[i][1]].append(arcs[i][0])

	for i in range(max_steps):
		#randomly choose a conflict variable from the node_values
		var = getVar(nodes, node_values, arcs, node_neigh)
		if var == -1:
			return node_values

		value = getValue(nodes, node_values, var, node_neigh)
		node_values[var] = value

	return []


#nodes, arcs, max_steps = 'CHTPS', [(0,1), (0,2), (1,2), (1,3), (1,4), (2,3), (2,4)], 1000
#nodes, arcs, max_steps = 'CTSHP', [(0,1), (0,2), (1,3), (2,4)], 1000
#nodes, arcs, max_steps = 'PTSCH', [(0,1), (0,2), (1,3), (2,3), (3,4)], 1000
#nodes, arcs, max_steps = 'TSCPH', [(0,1), (0,2), (1,3), (2,3), (3,4)], 1000
nodes, arcs, max_steps = 'CHTSP', [(0,1), (0,2), (1,3), (2,3), (3,4), (1,2)], 1000
print(solve_csp(nodes, arcs, max_steps))