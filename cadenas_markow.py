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
		for i in range(0,n):
			row_matrix.append(float(row_line[i]))
		M.append(row_matrix)
	return M

#Funcion que eleva una matriz a la n
def matrix_n_steps(M,steps):
	#Elevar M^stepts
	return linalg.matrix_power(M,steps)

#Funcion que multiplica un vector de probabilidad por la matriz correspondiente a la n
def probability_n_steps(p0,M,steps):
	#Elevar M^steps
	Mn = linalg.matrix_power(M,steps)
	global n
	vector = []
	#Realizar la multiplicacion de vector por matriz
	for i in range(0,n):
		row = 0
		for j in range(0,n):
			row = row + Mn[j][i]*p0[j]
		vector.append(row)
	return vector 

#Funcion que multiplica un vector de estado inicial por la matriz correspondiente a la n
def state_n_steps(p0,M,steps):
	#Elevar M^steps
	Mn = linalg.matrix_power(M,steps)
	global n
	vector = []
	#Realizar la multiplicacion de vector por matriz
	for i in range(0,n):
		row = 0
		for j in range(0,n):
			row = row + Mn[j][i]*p0[j]
		vector.append(row)
	return vector 

#Funcion que devuelve la matriz que se usa para resolver el sistema que lleva a estado estable
def get_linear_system(M):
	global n
	pi = []

	#Generar una matriz de puros 0 donde estara el sistema
	for i in range(0,n):
		row = []
		for j in range(0,n):
			row.append(0)
		pi.append(row)

	#Llenar con los valores de la matriz de probabilidades, eliminando la ultima ecuacion
	for i in range (0,n):
		for j in range(0,n):
			pi[j][i] = M[i][j]
			#Al elemento de la diagonal se le resta 1
			if (j == i):
				pi[i][j] = pi[i][j] - 1

	#Agregar fila de 1 al final del sistema
	for i in range (0,n):
		pi[n-1][i] = 1

	return pi

#Funcion que para una matriz devuelve su vector de estado estable
def stable_vector(M):
	
	#Obtener sistema a resolver
	pi = get_linear_system(M)

	#Si el determinante es 0, entonces no tiene solucion
	det = linalg.det(pi)
	if (det == 0):
		print "No tiene solucion"
		return []

	#Generar vector de respuestas para solucionar sistema
	b = []
	for i in range (0,n-1):
		b.append(0)

	b.append(1)

	#Resolver el sistema y retornar el valor
	pi = linalg.solve(pi,b)
	return pi

#Funcion que determina si una matriz ya se encuentra estabilizada
def calculate_stabilization(M,error):
	global n
	stable = True

	#Revisar si las filas son iguales comparando cada elemento con la primera fila
	for i in range(1,n):
		for j in range(0,n):
			#Se debe considerar un error, mientras menor sea mayor precision
			stable = stable and (abs(M[i][j]-M[1][j]) < error)
			if (not stable):
				return False

	return True


#Funcion que devuelve cuantas iteraciones son necesarias para estabilizar
def iterations_until_stabilization(M):

	pi = get_linear_system(M)

	#Si el sistema no tiene solucion entonces no se puede regresar respuesta
	det = linalg.det(pi)
	if (det == 0):
		print "No es posible estabilizar"
		return [[], 0]

	total = 1
	stable = False
	#Multiplica la matriz hasta tener una matriz estabilizada
	#Devuelve un tupla con la matriz estabilizada y la cantidad de iteraciones que se necesitaron
	while (not stable):
		Mn = matrix_n_steps(M,total)
		if (calculate_stabilization(Mn,0.0001)):
			return [Mn, total]
		total = total + 1

	return [Mn, total]

#Menu principal
def menu():
	global n
	#Lectura de la matriz con que se va a trabajar
	matrix_file = raw_input("Seleccione la matrix a utilizar: ")
	M = read_matrix(matrix_file)
	print "La matriz obtenida es: "
	print M
	option = -1
	while (option != 0):
		#Desplegar opciones
		print "\n\n+++++++CADENAS DE MARKOW++++++++"
		print "1. Leer otra matriz"
		print "2. Obtener vector de estado estable"
		print "3. Matrix de probabilidad de n pasos"
		print "4. Para vector de probabilidades inicial, probabilidades despues de n pasos"
		print "5. Para vector de estado inicial, estado despues de n pasos"
		print "6. Para vector de estado inicial, estado promedio cuando se estabiliza"
		print "0. Salir"
		option = int(raw_input("Introduzca su opcion: "))

		#Leer otra matriz
		if (option == 1):
			matrix_file = raw_input("Seleccione la matrix a utilizar: ")
			M = read_matrix(matrix_file)
			print "La matriz obtenida es: "
			print M

		#Calcular vector de estado estable
		elif (option == 2):
			stable = stable_vector(M)
			if (len(stable)>0):
				print "EL vector de estado estable es: "
				print stable
			else:
				print "Sin solucion: el sistema no se estabiliza"

		#Calcular matriz de n pasos
		elif (option == 3):
			steps = int(raw_input("Introduzca los n pasos deseados: "))
			matrix_steps = matrix_n_steps(M,steps)
			print "La matriz de " + str(steps) + " pasos es: "
			print matrix_steps

		#Probabilidad vector de n pasos
		elif (option == 4):
			initial_vector = []
			for i in range(0,n):
				initial_vector.append(float(raw_input("Vector["+str(i)+"]")))
			steps = int(raw_input("Introduzca los n pasos deseados: "))
			vector = probability_n_steps(initial_vector,M,steps)
			print "El vector tras " + str(steps) + " pasos es: "
			print vector

		#Calcular vector de n pasos
		elif (option == 5):
			initial_vector = []
			for i in range(0,n):
				initial_vector.append(int(raw_input("Vector["+str(i)+"]")))
			steps = int(raw_input("Introduzca los n pasos deseados: "))
			vector = state_n_steps(initial_vector,M,steps)
			print "El vector tras " + str(steps) + " pasos es: "
			print vector

		#Dado un estado inicial y la matriz de estado estable, calcula el estado promedio
		elif (option == 6):
			#Calcular la matriz de estado estable
			matrix_iterations = iterations_until_stabilization(M)
			stable_matrix = matrix_iterations[0]
			if (len(stable_matrix) > 0):
				print "Matriz de estado estable: "
				print stable_matrix
				print "Se necesitaron " + str(matrix_iterations[1]) + " iteraciones para llegar a la solucion"
				#Recibir el vector inicial
				initial_vector = []
				for i in range(0,n):
					initial_vector.append(int(raw_input("Vector["+str(i)+"]")))
				#Realizar el calculo
				vector = state_n_steps(initial_vector,M,1)
				print "El vector de estado promedio es: "
				print vector
			else:
				print "Sin solucion: el sistema no se estabiliza"

		#Salir del programa
		elif (option == 0):
			print "Gracias por usar el programa, hasta pronto"

		#Error
		else:
			print "Error: opcion incorrecta"

#Llamada al menu principal
menu()

