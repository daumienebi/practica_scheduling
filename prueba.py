'''
5 2
0 5 1 3
0 2 1 7
0 9 1 1
0 0 1 6
0 8 1 4

'''

#Pedir nombre del archivo
nombre_archivo = "prueba.txt"
f = open(nombre_archivo)

num_ordenes = f.read(1) # leer el numero de maquinas
num_maquinas = f.read(2) # movemos el cursor dos veces para leer el numeros de maquinas

rows = int(num_ordenes)
cols = int(num_maquinas)

matrizD = []
num_lineas = len(fp.readlines())
for i in range(num_lineas):
    linea = f.readline().split(" ")
    
        


'''
matriz[i][1]
matriz[i][3]
#estos serian d[i][j]

# ahora para las ordenes..una lista
list lista_ordenes = list(num_ordenes);


def Flowshop(lista_ordenes,matriz_d):

    return F_matriz

print("Hola mundo")
'''
