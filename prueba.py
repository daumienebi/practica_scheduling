import random



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


def calcular_F(secuencia, d):
    """
    Calcula la matriz de tiempos de finalización F.
    Las filas son máquinas y las columnas son las posiciones de los trabajos
    en la secuencia.
    """
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


def calcular_makespan(secuencia, d):
    """Devuelve el makespan de una secuencia."""
    F = calcular_F(secuencia, d)
    return F[-1][-1]


def generar_vecinos(secuencia):
    """Genera todos los vecinos intercambiando dos posiciones distintas."""
    vecinos = []
    n = len(secuencia)

    for i in range(n - 1):
        for j in range(i + 1, n):
            vecino = secuencia.copy()
            vecino[i], vecino[j] = vecino[j], vecino[i]
            vecinos.append(vecino)

    return vecinos


def busqueda_local(d, n):
    """Búsqueda local de mejor mejora, siguiendo el pseudocódigo del profesor."""
    # Crear una solución inicial aleatoria.
    secuencia = list(range(n))
    random.shuffle(secuencia)
    makespan_actual = calcular_makespan(secuencia, d)

    while True:
        # Determinar el vecindario completo de la solución actual.
        vecinos = generar_vecinos(secuencia)
        mejor_vecino = None
        mejor_makespan = makespan_actual

        # Evaluar todos los vecinos y guardar el mejor que mejore la solución.
        for vecino in vecinos:
            makespan_vecino = calcular_makespan(vecino, d)

            if makespan_vecino < mejor_makespan:
                mejor_makespan = makespan_vecino
                mejor_vecino = vecino

        # Si no hay mejora, se ha alcanzado un óptimo local.
        if mejor_vecino is None:
            break

        # Sustituir la solución actual por el mejor vecino.
        secuencia = mejor_vecino
        makespan_actual = mejor_makespan

    return secuencia, makespan_actual


def main():
    try:
        m, n, d = leer_archivo()

        secuencia, makespan = busqueda_local(d, n)
        F = calcular_F(secuencia, d)

        print("\n--- RESULTADOS ---")
        print("Número de máquinas:", m)
        print("Número de trabajos:", n)

        print("\nMatriz de tiempos de procesamiento d (filas = trabajos):")
        for fila in d:
            print(fila)

        print("\nSecuencia encontrada:", [trabajo + 1 for trabajo in secuencia])

        print("\nMatriz de tiempos de finalización F (filas = máquinas):")
        for fila in F:
            print(fila)

        print("\nMakespan (Fmax):", makespan)

    except (OSError, ValueError, IndexError) as error:
        print("Error al leer o procesar el archivo:", error)


if __name__ == "__main__":
    main()
