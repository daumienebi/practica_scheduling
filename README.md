# Práctica de Scheduling: Flow Shop Permutacional

Este proyecto resuelve el problema de programación de la producción en taller de flujo (**Flow Shop Permutacional**) minimizando el tiempo total de finalización o *makespan* ($F_{max}$). 

Incluye la implementación de 4 técnicas de optimización y metaheurísticas:
1. **Búsqueda Aleatoria**
2. **Búsqueda Local** (*Steepest Descent* / Mejor Mejora con vecindad por intercambio de dos trabajos)
3. **Recocido Simulado** (*Simulated Annealing* con enfriamiento geométrico y criterio de Metropolis)
4. **Algoritmo Genético** (Selección por torneo binario, cruce de orden OX, mutación *swap* y elitismo)

El cálculo de la matriz de tiempos de finalización $F_{ij}$ sigue la formulación matemática explicada en `Introducción a la F.pdf`.

---

## Requisitos e Instalación

Para ejecutar la aplicación localmente, asegúrate de tener **Python 3.10 o superior** instalado.

Instala las dependencias necesarias con pip:

```bash
pip install streamlit pandas altair
```

---

## Cómo Ejecutar

El proyecto cuenta con dos modos de ejecución:

### 1. Interfaz Web (Recomendada)
Para abrir la interfaz visual interactiva en tu navegador:

```bash
streamlit run app.py
```

Una vez ejecutado el comando, se abrirá automáticamente en tu navegador la dirección:
**http://localhost:8501**

Desde la web podrás:
- Seleccionar instancias de prueba (`prueba.txt` de 5 trabajos y 2 máquinas o `prueba2.txt` de 10 trabajos y 3 máquinas).
- Subir tus propios archivos `.txt` de datos.
- Ejecutar cualquier algoritmo individualmente o usar la opción **Comparar todos los algoritmos**.
- Visualizar las matrices $d_{ij}$ y $F_{ij}$, las métricas de mejora y un **diagrama de Gantt interactivo**.

---

### 2. Modo Consola
Si prefieres interactuar mediante la consola de comandos estándar:

```bash
python main.py
```

El programa te solicitará:
1. El nombre del fichero de datos (por ejemplo, `prueba.txt`).
2. La opción del algoritmo a ejecutar (1 a 4).
3. Mostrará en texto la secuencia inicial, la mejor secuencia obtenida, la matriz $F_{ij}$ y el $F_{max}$.

---

## Estructura del Proyecto

- `main.py`: Lógica de cálculo de tiempos ($F$), evaluación de $F_{max}$, funciones de lectura y los 4 algoritmos de optimización.
- `app.py`: Aplicación web construida con Streamlit.
- `prueba.txt`: Instancia de ejemplo del PDF (5 órdenes, 2 máquinas).
- `prueba2.txt`: Instancia extendida (10 órdenes, 3 máquinas).
- `Introducción a la F.pdf`: Documento de referencia con la formulación del problema y el ejemplo resuelto.

