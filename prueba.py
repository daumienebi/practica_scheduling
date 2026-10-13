import random
import math


def leer_archivo():

    nombre_archivo = input("Nombre del archivo: ")

    with open(nombre_archivo, "r") as archivo:
        lineas = archivo.readlines()

    # Leer el numero de trabajos y maquinas
    primera_linea = lineas[0].split()
    n = int(primera_linea[0])
    m = int(primera_linea[1])

    # Leer los tiempos de procesamiento
    d = []

    for linea in lineas[1:]:
        valores = linea.split()
        tiempos = []

        for j in range(1, len(valores), 2):
            tiempos.append(int(valores[j]))

        d.append(tiempos)

    return m, n, d

"""
    Calcula la matriz de tiempos de finalización F.
    Las filas son máquinas y las columnas son las posiciones de los trabajos
    en la secuencia.
"""
def calcular_Funcion_F(secuencia, d):
    n = len(secuencia)
    m = len(d[0])
    F = [[0 for _ in range(n)] for _ in range(m)]

    for i in range(m):
        for j in range(n):
            trabajo = secuencia[j]  # Índice del trabajo, empezando en 0.
            tiempo = d[trabajo][i]

            if i == 0 and j == 0:
                F[i][j] = tiempo
            elif i == 0:
                F[i][j] = F[i][j - 1] + tiempo
            elif j == 0:
                F[i][j] = F[i - 1][j] + tiempo
            else:
                F[i][j] = max(F[i - 1][j], F[i][j - 1]) + tiempo

    return F

"""Devuelve el fmax de una secuencia."""
def calcular_fmax(secuencia, d):
    F = calcular_Funcion_F(secuencia, d)
    fmax = F[-1][-1]
    return fmax

"""Genera todos los vecinos intercambiando dos posiciones distintas."""
def generar_vecinos(secuencia):
    vecinos = []
    n = len(secuencia)

    for i in range(n - 1):
        for j in range(i + 1, n):
            vecino = secuencia.copy()
            vecino[i], vecino[j] = vecino[j], vecino[i]
            vecinos.append(vecino)

    return vecinos

"""Búsqueda local de mejor mejora."""
def busqueda_local(d, n):
    # Crear una solución inicial aleatoria.
    secuencia = list(range(n))
    random.shuffle(secuencia)
    fmax_actual = calcular_fmax(secuencia, d)

    while True:
        # Determinar el vecindario completo de la solución actual.
        vecinos = generar_vecinos(secuencia)
        mejor_vecino = None
        mejor_fmax = fmax_actual

        # Evaluar todos los vecinos y guardar el mejor que mejore la solución.
        for vecino in vecinos:
            fmax_vecino = calcular_fmax(vecino, d)

            if fmax_vecino < mejor_fmax:
                mejor_fmax = fmax_vecino
                mejor_vecino = vecino

        # Si no hay mejora, se ha alcanzado un óptimo local.
        if mejor_vecino is None:
            break

        # Sustituir la solución actual por el mejor vecino.
        secuencia = mejor_vecino
        fmax_actual = mejor_fmax

    return secuencia, fmax_actual


def algoritmo_recocido_simulado(d,n):
    # Crear una solución inicial y cal Fmax
    secuencia = list(range(n))
    random.shuffle(secuencia)
    fmax_actual = calcular_fmax(secuencia,d)

    # Guardar la mejor solucion encontrada
    mejor_secuencia = secuencia.copy()
    mejor_fmax = fmax_actual

    #definir las valores iniciales de los parámetros de control
    T_inicial = 1000
    level_length = 100
    alpha = 0,95
    nivel = 0
    max_nivel = 100


    # Repetir mientras no se alcance el limite de niveles
    while nivel < max_nivel and T_inicial > 0.001:

        # Realizar L intentos a esta temperatura
        for i in range(level_length):

            # Crear un vecino intercambiando dos trabajos
            vecino = secuencia.copy()

            if n > 1:
                pos1 = random.randint(0, n - 1)
                pos2 = random.randint(0, n - 1)

                while pos1 == pos2:
                    pos2 = random.randint(0, n - 1)

                vecino[pos1], vecino[pos2] = (vecino[pos2], vecino[pos1])

            # Calcular la diferencia entre las soluciones
            fmax_vecino = calcular_fmax(vecino, d)
            delta = fmax_vecino - fmax_actual

            # Aceptar siempre si mejora o mantiene el valor
            if delta <= 0:
                secuencia = vecino
                fmax_actual = fmax_vecino

            else:
                # Aceptar una solucion peor con cierta probabilidad
                probabilidad = math.exp(-delta / T_inicial)
                r = random.random()

                if r <= probabilidad:
                    secuencia = vecino
                    fmax_actual = fmax_vecino

        # Actualizar la mejor solucion encontrada
        if fmax_actual < mejor_fmax:
            mejor_secuencia = secuencia.copy()
            mejor_fmax = fmax_actual

        # Enfriar el sistema
        T_inicial = T_inicial * alpha
        nivel = nivel + 1

    return mejor_secuencia, mejor_fmax
        






def main():

    # Leer el archivo
    m, n, d = leer_archivo()

    # Elegir el algoritmo
    print("\nElige el algoritmo:")
    print("1. Algoritmo de búsqueda aleatoria")
    print("2. Algoritmo de búsqueda local")
    print("3. Algoritmo de recocido simulado")
    print("4. Algoritmo Genético")

    opcion = input("Introduce una opcion (1 o 2): ")

    match opcion:
        case "1":
            #secuencia, fmax = busqueda_aleatoria(d, n)
            nombre_algoritmo = "Algoritmo de búsqueda aleatoria"
        case "2":
            secuencia, fmax = busqueda_local(d, n)
            nombre_algoritmo = "Algoritmo de búsqueda local del mejor"
        case "3":
            secuencia, fmax = algoritmo_recocido_simulado(d, n)
            nombre_algoritmo = "Algoritmo de recocido simulado"
        case "4":
            secuencia, fmax = algoritmo_recocido_simulado(d, n)
            nombre_algoritmo = "Algoritmo de recocido simulado"
        case _:
            print("Opcion no valida.")
            return

    # Calcular la matriz de tiempos de finalizacion
    F = calcular_Funcion_F(secuencia, d)

    # Mostrar los resultados
    print("\n--- RESULTADOS ---")
    print("Algoritmo utilizado:", nombre_algoritmo)
    print("Numero de maquinas:", m)
    print("Numero de trabajos:", n)

    print("\nSecuencia encontrada:")
    print([trabajo + 1 for trabajo in secuencia])

    print("\nMatriz de tiempos de finalizacion F:")
    for fila in F:
        print(fila)

    print("\nFmax:", fmax)


if __name__ == "__main__":
    main()
