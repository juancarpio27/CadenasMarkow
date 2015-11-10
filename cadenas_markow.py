import numpy.linalg as linalg

n = 0;

def read_matrix(file):
	matrix_file = open(file,'r')
	global  n
	n = matrix_file.readline()
	n = int(n)
	M = []
	for line in matrix_file:
		row_line = line.split()
		row_matrix = []
		for i in range(0,3):
			row_matrix.append(float(row_line[i]))
		M.append(row_matrix)
	return M

def matrix_n_steps(M,steps):
	return linalg.matrix_power(M,steps)

def probability_n_steps(p0,M,steps):
	Mn = linalg.matrix_power(M,steps)


M = read_matrix('matrix.txt')


