import streamlit as st
import random
import pandas as pd
import altair as alt
import main

st.set_page_config(
    page_title="Flow Shop Scheduling",
    page_icon="",
    layout="wide"
)

def parsear_datos(texto):
    """Parsea el contenido de texto de una instancia de flow shop."""
    lineas = [l for l in texto.strip().splitlines() if l.strip()]
    if not lineas:
        return None, None, None
    primera_linea = lineas[0].split()
    num_trabajos = int(primera_linea[0])
    num_maquinas = int(primera_linea[1])
    d = []
    for linea in lineas[1:]:
        valores = linea.split()
        if not valores:
            continue
        if len(valores) >= 2 * num_maquinas:
            tiempos = [int(valores[j]) for j in range(1, 2 * num_maquinas, 2)]
        else:
            tiempos = [int(v) for v in valores[:num_maquinas]]
        d.append(tiempos)
    return num_maquinas, num_trabajos, d

def crear_df_gantt(secuencia, d, F):
    """Construye los intervalos [inicio, fin] de cada operación para el diagrama de Gantt."""
    filas = []
    m = len(d[0])
    for maq in range(m):
        for trabajo in secuencia:
            duracion = d[trabajo][maq]
            fin = F[trabajo][maq]
            inicio = fin - duracion
            if duracion > 0:
                filas.append({
                    "Máquina": f"Máquina {maq + 1}",
                    "Trabajo": f"Trabajo {trabajo + 1}",
                    "Inicio": inicio,
                    "Fin": fin,
                    "Duración": duracion
                })
    return pd.DataFrame(filas)

st.title("⏱️ Flow Shop Permutacional - Scheduling")

# --- BARRA LATERAL ---
st.sidebar.header("1. Entrada de Datos")
fuente_archivo = st.sidebar.radio(
    "Selecciona archivo:",
    ("prueba.txt (5 trab., 2 máq.)", "prueba2.txt (10 trab., 3 máq.)", "Subir archivo .txt")
)

contenido = None
if "prueba.txt" in fuente_archivo:
    try:
        with open("prueba.txt", "r") as f:
            contenido = f.read()
    except Exception as e:
        st.sidebar.error(f"Error al abrir prueba.txt: {e}")
elif "prueba2.txt" in fuente_archivo:
    try:
        with open("prueba2.txt", "r") as f:
            contenido = f.read()
    except Exception as e:
        st.sidebar.error(f"Error al abrir prueba2.txt: {e}")
else:
    archivo_subido = st.sidebar.file_uploader("Selecciona un fichero .txt", type=["txt"])
    if archivo_subido is not None:
        contenido = archivo_subido.getvalue().decode("utf-8")

if contenido:
    m, n, d = parsear_datos(contenido)
    st.sidebar.success(f"Instancia: **{n} trabajos**, **{m} máquinas**")

    st.sidebar.header("2. Algoritmo")
    algoritmo = st.sidebar.selectbox(
        "Elige el algoritmo:",
        (
            "1. Algoritmo de búsqueda aleatoria",
            "2. Algoritmo de búsqueda local",
            "3. Algoritmo de recocido simulado",
            "4. Algoritmo Genético",
            "5. Comparar todos los algoritmos"
        )
    )

    num_iter_ba = 100
    if "aleatoria" in algoritmo or "Comparar" in algoritmo:
        num_iter_ba = st.sidebar.number_input(
            "Iteraciones (Búsqueda Aleatoria):",
            min_value=10,
            max_value=100000,
            value=200,
            step=50
        )

    ejecutar = st.sidebar.button("Ejecutar Algoritmo", type="primary", use_container_width=True)

    # --- PESTAÑAS / COLUMNAS ---
    col_izq, col_der = st.columns([1, 2])

    with col_izq:
        st.subheader("Matriz de Tiempos $d_{ij}$")
        columnas_d = [f"Máq {j+1}" for j in range(m)]
        filas_d = [f"Trabajo {i+1}" for i in range(n)]
        df_d = pd.DataFrame(d, index=filas_d, columns=columnas_d)
        st.dataframe(df_d, use_container_width=True)

    with col_der:
        st.subheader("Resultados")

        if ejecutar:
            # Secuencia inicial aleatoria común para comparar equitativamente
            secuencia_inicial = list(range(n))
            random.shuffle(secuencia_inicial)
            fmax_inicial = main.calcular_fmax(secuencia_inicial, d)

            if "Comparar" in algoritmo:
                with st.spinner("Ejecutando todos los algoritmos..."):
                    sec_ba, f_ba = main.busqueda_aleatoria(d, n, secuencia_inicial, numero_iteraciones=num_iter_ba)
                    sec_bl, f_bl = main.busqueda_local(d, n, secuencia_inicial)
                    sec_rs, f_rs = main.algoritmo_recocido_simulado(d, n, secuencia_inicial)
                    sec_ag, f_ag = main.algoritmo_genetico(d, n, secuencia_inicial)

                df_comp = pd.DataFrame([
                    {"Algoritmo": "Secuencia Inicial", "Secuencia (1-indexada)": str([t+1 for t in secuencia_inicial]), "Fmax": fmax_inicial},
                    {"Algoritmo": "1. Búsqueda Aleatoria", "Secuencia (1-indexada)": str([t+1 for t in sec_ba]), "Fmax": f_ba},
                    {"Algoritmo": "2. Búsqueda Local", "Secuencia (1-indexada)": str([t+1 for t in sec_bl]), "Fmax": f_bl},
                    {"Algoritmo": "3. Recocido Simulado", "Secuencia (1-indexada)": str([t+1 for t in sec_rs]), "Fmax": f_rs},
                    {"Algoritmo": "4. Algoritmo Genético", "Secuencia (1-indexada)": str([t+1 for t in sec_ag]), "Fmax": f_ag},
                ])
                st.table(df_comp)

                # Seleccionar el mejor para mostrar la matriz F y el Gantt
                mejores = [
                    (f_ba, sec_ba, "Búsqueda Aleatoria"),
                    (f_bl, sec_bl, "Búsqueda Local"),
                    (f_rs, sec_rs, "Recocido Simulado"),
                    (f_ag, sec_ag, "Algoritmo Genético")
                ]
                mejores.sort(key=lambda x: x[0])
                mejor_f, mejor_sec, mejor_nombre = mejores[0]

                st.success(f"🏆 Mejor resultado: **{mejor_nombre}** con **Fmax = {mejor_f}**")
                secuencia = mejor_sec
                fmax = mejor_f
            else:
                with st.spinner("Calculando..."):
                    if "1." in algoritmo:
                        secuencia, fmax = main.busqueda_aleatoria(d, n, secuencia_inicial, numero_iteraciones=num_iter_ba)
                    elif "2." in algoritmo:
                        secuencia, fmax = main.busqueda_local(d, n, secuencia_inicial)
                    elif "3." in algoritmo:
                        secuencia, fmax = main.algoritmo_recocido_simulado(d, n, secuencia_inicial)
                    elif "4." in algoritmo:
                        secuencia, fmax = main.algoritmo_genetico(d, n, secuencia_inicial)

                m_col1, m_col2, m_col3 = st.columns(3)
                m_col1.metric("Fmax Inicial", fmax_inicial)
                m_col2.metric("Mejor Fmax", fmax, delta=f"{fmax - fmax_inicial}", delta_color="inverse")
                mejora = ((fmax_inicial - fmax) / fmax_inicial * 100) if fmax_inicial else 0
                m_col3.metric("Mejora", f"{mejora:.1f}%")

                st.write(f"**Secuencia inicial:** `{[t + 1 for t in secuencia_inicial]}`")
                st.success(f"**Mejor secuencia:** `{[t + 1 for t in secuencia]}`")

            # Matriz de tiempos de finalización F
            F = main.calcular_Funcion_F(secuencia, d)
            st.markdown("#### Matriz de Tiempos de Finalización $F_{ij}$")
            columnas_f = [f"Máq {j+1}" for j in range(m)]
            filas_f = [f"Trabajo {i+1}" for i in range(n)]
            df_F = pd.DataFrame(F, index=filas_f, columns=columnas_f)
            st.dataframe(df_F, use_container_width=True)

            # Diagrama de Gantt
            st.markdown("#### Diagrama de Gantt")
            df_gantt = crear_df_gantt(secuencia, d, F)
            if not df_gantt.empty:
                orden_maquinas = [f"Máquina {j+1}" for j in range(m)]
                chart = (
                    alt.Chart(df_gantt)
                    .mark_bar(cornerRadius=3, stroke="black", strokeWidth=1)
                    .encode(
                        x=alt.X("Inicio:Q", title="Tiempo"),
                        x2="Fin:Q",
                        y=alt.Y("Máquina:N", title="Máquina", sort=orden_maquinas),
                        color=alt.Color("Trabajo:N", title="Trabajo", scale=alt.Scale(scheme="category10")),
                        tooltip=["Máquina", "Trabajo", "Inicio", "Fin", "Duración"]
                    )
                    .properties(height=100 + m * 50)
                )
                st.altair_chart(chart, use_container_width=True)

        else:
            st.info("Configura las opciones en el panel lateral y pulsa ** Ejecutar Algoritmo**.")
else:
    st.warning("Selecciona o sube un archivo para comenzar.")
