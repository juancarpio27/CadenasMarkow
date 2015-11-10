import numpy.linalg as linalg
import math

#Variable global para las dimensiones de la matriz
n = 0;

#Funcion para leer una matriz proveniente de un archivo de texto
def read_matrix(file):
	#Abrir el archivo
	matrix_file = open(file,'r')
	global  n

	#Leer la primera linea con las dimensiones de la matriz
	n = matrix_file.readline()
	n = int(n)
	M = []

	#Revisar linea por linea y agregar a la matriz
	for line in matrix_file:
		row_line = line.split()
		row_matrix = []
		for i in range(0,3):
			row_matrix.append(float(row_line[i]))
		M.append(row_matrix)
	return M

#Funcion que eleva una matriz a la n
def matrix_n_steps(M,steps):
	return linalg.matrix_power(M,steps)

#Funcion que multiplica un vector de probabilidad por la matriz correspondiente a la n
def probability_n_steps(p0,M,steps):
	Mn = linalg.matrix_power(M,steps)
	global n
	vector = []
	for i in range(0,n):
		row = 0
		for j in range(0,n):
			row = row + M[j][i]*p0[j]
		vector.append(row)
	return vector 

#Funcion que multiplica un vector de estado inicial por la matriz correspondiente a la n
def state_n_steps(p0,M,steps):
	Mn = linalg.matrix_power(M,steps)
	global n
	vector = []
	for i in range(0,n):
		row = 0
		for j in range(0,n):
			row = row + M[j][i]*p0[j]
		vector.append(row)
	return vector 

#Funcion que devuelve la matriz que se usa para resolver el sistema que lleva a estado estable
def get_linear_system(M):
	global n
	pi = []

	for i in range(0,n):
		row = []
		for j in range(0,n):
			row.append(0)
		pi.append(row)

	for i in range (0,n):
		for j in range(0,n):
			pi[j][i] = M[i][j]
			if (j == i):
				pi[i][j] = pi[i][j] - 1

	for i in range (0,n):
		pi[n-1][i] = 1

	return pi

#Funcion que para una matriz devuelve su vector de estado estable
def stable_vector(M):
	
	pi = get_linear_system(M)

	det = linalg.det(pi)
	if (det == 0):
		print "No tiene solucion"
		return []

	b = []
	for i in range (0,n-1):
		b.append(0)

	b.append(1)

	pi = linalg.solve(pi,b)
	return pi

#Funcion que determina si una matriz ya se encuentra estabilizada
def calculate_stabilization(M,error):
	global n
	stable = True

	for i in range(1,n):
		for j in range(0,n):
			stable = stable and (abs(M[i][j]-M[1][j]) < error)
			if (not stable):
				return False

	return True


#Funcion que devuelve cuantas iteraciones son necesarias para estabilizar
def iterations_until_stabilization(M):

	pi = get_linear_system(M)

	det = linalg.det(pi)
	if (det == 0):
		print "No es posible estabilizar"
		return 0

	total = 1
	stable = False
	while (not stable):
		Mn = matrix_n_steps(M,total)
		if (calculate_stabilization(Mn,0.0001)):
			print Mn
			return total
		total = total + 1

	return total

M = read_matrix('matrix.txt')

print iterations_until_stabilization(M)



