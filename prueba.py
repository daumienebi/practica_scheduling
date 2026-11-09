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
    Calcula la matriz de tiempos de finalización F (n x m).
    Las filas corresponden a cada trabajo (0..n-1) y las columnas a cada máquina (0..m-1),
    tal y como se define en 'Introducción a la F.pdf'.
"""
def calcular_Funcion_F(secuencia, d):
    n = len(secuencia)
    m = len(d[0])
    F = [[0 for _ in range(m)] for _ in range(n)]

    for pos in range(n):
        trabajo = secuencia[pos]
        trabajo_ant = secuencia[pos - 1] if pos > 0 else None

        for maq in range(m):
            tiempo = d[trabajo][maq]

            if pos == 0 and maq == 0:
                F[trabajo][maq] = tiempo
            elif pos == 0:
                F[trabajo][maq] = F[trabajo][maq - 1] + tiempo
            elif maq == 0:
                F[trabajo][maq] = F[trabajo_ant][maq] + tiempo
            else:
                F[trabajo][maq] = max(F[trabajo_ant][maq], F[trabajo][maq - 1]) + tiempo

    return F

"""Devuelve el fmax (makespan) de una secuencia."""
def calcular_fmax(secuencia, d):
    F = calcular_Funcion_F(secuencia, d)
    ultimo_trabajo = secuencia[-1]
    fmax = F[ultimo_trabajo][-1]
    return fmax

"""Genera todos los vecinos intercambiando dos posiciones distintas (operador swap)."""
def generar_vecinos(secuencia):
    vecinos = []
    n = len(secuencia)

    for i in range(n - 1):
        for j in range(i + 1, n):
            vecino = secuencia.copy()
            vecino[i], vecino[j] = vecino[j], vecino[i]
            vecinos.append(vecino)

    return vecinos

"""Búsqueda local de mejor mejora (Steepest Descent)."""
def busqueda_local(d, n, secuencia_inicial=None):
    # Crear una solución inicial aleatoria si no se proporciona una.
    if secuencia_inicial is None:
        secuencia = list(range(n))
        random.shuffle(secuencia)
    else:
        secuencia = secuencia_inicial.copy()

    fmax_actual = calcular_fmax(secuencia, d)

    while True:
        # Determinar el vecindario completo de la solución actual.
        vecinos = generar_vecinos(secuencia)
        mejor_vecino = None
        mejor_fmax = fmax_actual

        # Evaluar todos los vecinos y guardar el que más mejore la solución.
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


"""Algoritmo de Recocido Simulado (Simulated Annealing)."""
def algoritmo_recocido_simulado(d, n, secuencia_inicial=None):
    # Crear una solución inicial y calcular su Fmax
    if secuencia_inicial is None:
        secuencia = list(range(n))
        random.shuffle(secuencia)
    else:
        secuencia = secuencia_inicial.copy()

    fmax_actual = calcular_fmax(secuencia, d)

    # Guardar la mejor solución encontrada hasta el momento
    mejor_secuencia = secuencia.copy()
    mejor_fmax = fmax_actual

    # Definir los valores iniciales de los parámetros de control
    T_inicial = 1000
    level_length = 100
    alpha = 0.95
    nivel = 0
    max_nivel = 100

    # Repetir mientras no se alcance el límite de niveles ni temperatura mínima
    while nivel < max_nivel and T_inicial > 0.001:
        # Realizar L intentos a esta temperatura
        for i in range(level_length):
            # Crear un vecino intercambiando dos trabajos al azar
            vecino = secuencia.copy()
            if n > 1:
                pos1 = random.randint(0, n - 1)
                pos2 = random.randint(0, n - 1)
                while pos1 == pos2:
                    pos2 = random.randint(0, n - 1)
                vecino[pos1], vecino[pos2] = vecino[pos2], vecino[pos1]

            # Calcular la diferencia de coste entre el vecino y la solución actual
            fmax_vecino = calcular_fmax(vecino, d)
            delta = fmax_vecino - fmax_actual

            # Aceptar siempre si mejora o iguala el valor actual
            if delta <= 0:
                secuencia = vecino
                fmax_actual = fmax_vecino

                # Actualizar la mejor solución global inmediatamente si hemos mejorado
                if fmax_actual < mejor_fmax:
                    mejor_secuencia = secuencia.copy()
                    mejor_fmax = fmax_actual
            else:
                # Aceptar una solución peor con probabilidad e^(-delta / T)
                probabilidad = math.exp(-delta / T_inicial)
                r = random.random()

                if r <= probabilidad:
                    secuencia = vecino
                    fmax_actual = fmax_vecino

        # Enfriar el sistema
        T_inicial = T_inicial * alpha
        nivel = nivel + 1

    return mejor_secuencia, mejor_fmax

def busqueda_aleatoria(d, n, secuencia_inicial=None):
    """
    Búsqueda aleatoria: genera secuencias al azar durante un número de iteraciones
    y conserva aquella que obtiene el mejor (menor) Fmax.
    """
    numero_iteraciones = int(input("¿Cuántas iteraciones?: "))

    # Solución inicial
    if secuencia_inicial is None:
        secuencia = list(range(n))
        random.shuffle(secuencia)
    else:
        secuencia = secuencia_inicial.copy()

    solucion_actual = calcular_fmax(secuencia, d)
    mejor_solucion = solucion_actual
    mejor_secuencia = secuencia.copy()

    # Repetición durante el número de iteraciones indicadas
    for i in range(numero_iteraciones):
        # Generamos una nueva secuencia aleatoria y calculamos su Fmax
        random.shuffle(secuencia)
        solucion_actual = calcular_fmax(secuencia, d)

        # Buscamos minimizar el tiempo de finalización (menor Fmax es mejor)
        if solucion_actual < mejor_solucion:
            mejor_solucion = solucion_actual
            mejor_secuencia = secuencia.copy()

    return mejor_secuencia, mejor_solucion


"""
    Operador de Cruce de Orden (OX - Order Crossover) para permutaciones.
    Copia un segmento del padre1 y rellena el resto respetando el orden del padre2
    sin repetir trabajos.
"""
def cruce_orden(padre1, padre2):
    n = len(padre1)
    if n < 2:
        return padre1.copy()

    # Elegir dos puntos de corte aleatorios
    punto1, punto2 = sorted(random.sample(range(n), 2))

    # Crear hijo vacío y copiar el segmento del padre1
    hijo = [None] * n
    hijo[punto1:punto2 + 1] = padre1[punto1:punto2 + 1]

    # Completar con los trabajos del padre2 que aún no estén en el hijo
    pos_hijo = 0
    for trabajo in padre2:
        if trabajo not in hijo:
            while hijo[pos_hijo] is not None:
                pos_hijo += 1
            hijo[pos_hijo] = trabajo

    return hijo


"""
    Algoritmo Genético para el problema de Flow Shop Scheduling.
    Utiliza selección por torneo binario, cruce de orden (OX), mutación por
    intercambio (swap) y elitismo.
"""
def algoritmo_genetico(d, n, secuencia_inicial=None):
    # Parámetros del algoritmo genético
    tam_poblacion = 20
    num_generaciones = 100
    prob_cruce = 0.8
    prob_mutacion = 0.2

    # 1. Inicializar la población con secuencias aleatorias
    poblacion = []
    if secuencia_inicial is not None:
        poblacion.append(secuencia_inicial.copy())

    while len(poblacion) < tam_poblacion:
        individuo = list(range(n))
        random.shuffle(individuo)
        poblacion.append(individuo)

    # Evaluar la población inicial y guardar el mejor individuo global
    costes = [calcular_fmax(ind, d) for ind in poblacion]
    idx_mejor = costes.index(min(costes))
    mejor_secuencia = poblacion[idx_mejor].copy()
    mejor_fmax = costes[idx_mejor]

    # 2. Bucle evolutivo a lo largo de las generaciones
    for gen in range(num_generaciones):
        # Elitismo: el mejor individuo pasa directamente a la siguiente generación
        nueva_poblacion = [mejor_secuencia.copy()]

        while len(nueva_poblacion) < tam_poblacion:
            # Selección por torneo binario para escoger dos padres
            i1, i2 = random.sample(range(tam_poblacion), 2)
            padre1 = poblacion[i1] if costes[i1] <= costes[i2] else poblacion[i2]

            j1, j2 = random.sample(range(tam_poblacion), 2)
            padre2 = poblacion[j1] if costes[j1] <= costes[j2] else poblacion[j2]

            # Cruce (con probabilidad prob_cruce)
            if random.random() < prob_cruce:
                hijo = cruce_orden(padre1, padre2)
            else:
                hijo = padre1.copy()

            # Mutación por intercambio de dos posiciones (con probabilidad prob_mutacion)
            if n > 1 and random.random() < prob_mutacion:
                pos1, pos2 = random.sample(range(n), 2)
                hijo[pos1], hijo[pos2] = hijo[pos2], hijo[pos1]

            nueva_poblacion.append(hijo)

        # Actualizar la población y volver a evaluar los costes (Fmax)
        poblacion = nueva_poblacion
        costes = [calcular_fmax(ind, d) for ind in poblacion]

        # Actualizar la mejor solución encontrada
        mejor_gen_fmax = min(costes)
        if mejor_gen_fmax < mejor_fmax:
            mejor_fmax = mejor_gen_fmax
            mejor_secuencia = poblacion[costes.index(mejor_gen_fmax)].copy()

    return mejor_secuencia, mejor_fmax


def main():
    # Leer el archivo de entrada
    m, n, d = leer_archivo()

    # Generar la secuencia inicial aleatoria común para poder compararla con el resultado
    secuencia_inicial = list(range(n))
    random.shuffle(secuencia_inicial)
    fmax_inicial = calcular_fmax(secuencia_inicial, d)

    # Elegir el algoritmo
    print("\nElige el algoritmo:")
    print("1. Algoritmo de búsqueda aleatoria")
    print("2. Algoritmo de búsqueda local")
    print("3. Algoritmo de recocido simulado")
    print("4. Algoritmo Genético")

    opcion = input("Introduce una opcion (1-4): ")

    if opcion == "1":
        secuencia, fmax = busqueda_aleatoria(d, n, secuencia_inicial)
        nombre_algoritmo = "Algoritmo de búsqueda aleatoria"
    elif opcion == "2":
        secuencia, fmax = busqueda_local(d, n, secuencia_inicial)
        nombre_algoritmo = "Algoritmo de búsqueda local del mejor"
    elif opcion == "3":
        secuencia, fmax = algoritmo_recocido_simulado(d, n, secuencia_inicial)
        nombre_algoritmo = "Algoritmo de recocido simulado"
    elif opcion == "4":
        secuencia, fmax = algoritmo_genetico(d, n, secuencia_inicial)
        nombre_algoritmo = "Algoritmo Genético"
    else:
        print("Opcion no valida.")
        return
        
    # Calcular la matriz de tiempos de finalización F de la mejor secuencia encontrada
    F = calcular_Funcion_F(secuencia, d)
    
    # Mostrar los resultados
    print("\n--- RESULTADOS ---")
    print("Algoritmo utilizado:", nombre_algoritmo)
    print("Numero de maquinas:", m)
    print("Numero de trabajos:", n)

    print("\nSecuencia inicial:")
    print([trabajo + 1 for trabajo in secuencia_inicial], f"(Fmax inicial: {fmax_inicial})")

    print("\nMejor secuencia encontrada:")
    print([trabajo + 1 for trabajo in secuencia])

    print("\nMatriz de tiempos de finalizacion F (filas = trabajos, columnas = maquinas):")
    for fila in F:
        print(fila)

    print("\nFmax:", fmax)

if __name__ == "__main__":
    main()
