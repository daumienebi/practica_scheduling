# Práctica de Scheduling: Flow Shop Permutacional

Este proyecto resuelve el problema de programación de la producción en taller de flujo (**Flow Shop Permutacional**) minimizando el tiempo total de finalización o *makespan* ($F_{max}$). 

Incluye la implementación de 4 técnicas de optimización y metaheurísticas:
1. **Búsqueda Aleatoria**
2. **Búsqueda Local** (*Steepest Descent* / Mejor Mejora con vecindad por intercambio de dos trabajos)
3. **Recocido Simulado** (*Simulated Annealing* con enfriamiento geométrico y criterio de Metropolis)
4. **Algoritmo Genético** (Selección por torneo binario, cruce de orden OX, mutación *swap* y elitismo)

El cálculo de la matriz de tiempos de finalización $F_{ij}$ sigue la formulación matemática explicada en `Introducción a la F.pdf`.

---

## Cómo Ejecutar y Probar

Existen tres formas de probar la práctica, siendo la **Opción 1** la más rápida e inmediata:

### 1. Acceso Directo Online (Recomendado para evaluación — Sin instalación)
No requiere instalar Python ni ninguna librería en el ordenador. La aplicación web se encuentra desplegada y lista para usarse directamente en el navegador:

**[https://practicascheduling.streamlit.app/](https://practicascheduling.streamlit.app/)**

Desde la web interactiva podrás:
- Seleccionar directamente las instancias de prueba (`prueba.txt` de 5 trabajos y 2 máquinas o `prueba2.txt` de 10 trabajos y 3 máquinas).
- Subir cualquier otro archivo `.txt` de datos.
- Ejecutar cualquiera de los 4 algoritmos o usar la opción **Comparar todos los algoritmos** a la vez.
- Visualizar interactivamente las matrices $d_{ij}$ y $F_{ij}$, las métricas de mejora y el **diagrama de Gantt**.

---

### 2. Ejecución Local con Interfaz Web
Si se desea ejecutar la interfaz web de manera local en el propio equipo:

1. Asegúrate de tener Python 3.10 o superior instalado.
2. Instala las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   ```
3. Lanza la aplicación:
   ```bash
   streamlit run app.py
   ```
   Se abrirá automáticamente en tu navegador en `http://localhost:8501`.

---

### 3. Modo Consola (Terminal)
Si se prefiere interactuar mediante la consola de comandos estándar:

```bash
python main.py
```

El programa solicitará:
1. El nombre del fichero de datos (por ejemplo, `prueba.txt` o `prueba2.txt`).
2. El algoritmo a ejecutar (1 a 4).
3. Mostrará por terminal la secuencia inicial, la mejor secuencia encontrada, la matriz $F_{ij}$ y el $F_{max}$.

---

## 📁 Estructura del Proyecto

- `main.py`: Lógica de cálculo de tiempos ($F$), evaluación de $F_{max}$, funciones de lectura y los 4 algoritmos de optimización.
- `app.py`: Aplicación web interactiva construida con Streamlit.
- `requirements.txt`: Dependencias del proyecto (`streamlit`, `pandas`, `altair`).
- `prueba.txt`: Instancia de ejemplo del PDF (5 órdenes, 2 máquinas).
- `prueba2.txt`: Instancia extendida (10 órdenes, 3 máquinas).
- `Introducción a la F.pdf`: Documento de referencia con la formulación del problema y el ejemplo resuelto.
