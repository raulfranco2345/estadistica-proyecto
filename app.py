
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración básica de la página
st.set_page_config(page_title="App de Estadística e IA", layout="wide")

# Título y Créditos
st.title("📊 Documentación de Proceso Creativo")
st.markdown("### Estudiante: Franco Córdova Fabricio Raúl")
st.write("Objetivo: Evaluar las limitaciones de la IA en el desarrollo de software estadístico.")

st.divider()

# --- MÓDULO 1: CARGA DE DATOS ---
st.header("1. Carga de Datos")

opcion = st.radio(
    "Selecciona el origen de los datos:", 
    ["Generar datos sintéticos", "Subir archivo CSV"]
)

# Inicializamos el DataFrame como None
df = None

if opcion == "Generar datos sintéticos":
    # Generamos 100 números con una distribución normal (media 50, desv 10)
    datos_base = np.random.normal(loc=50, scale=10, size=100)
    df = pd.DataFrame(datos_base, columns=["Variable_Analizada"])
    st.success("✅ ¡Datos sintéticos generados con éxito!")
else:
    archivo = st.file_uploader("Sube tu archivo CSV", type=["csv"])
    if archivo is not None:
        df = pd.read_csv(archivo)
        st.success("✅ Archivo cargado correctamente")
    else:
        st.info("💡 Esperando a que subas un archivo CSV...")

# Solo mostramos la tabla si el DataFrame existe
if df is not None:
    st.subheader("Vista previa de los datos")
    st.dataframe(df.head(10)) # Muestra las primeras 10 filas
    
    # Información básica de la muestra
    st.write(f"**Tamaño de la muestra (n):** {len(df)}")

    # --- MÓDULO 2: ESTADÍSTICA DESCRIPTIVA ---
if df is not None:
    st.divider()
    st.header("2. Estadísticas Descriptivas")
    
    variable = df.columns[0] # Tomamos la primera columna
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Media", f"{df[variable].mean():.2f}")
    col2.metric("Mediana", f"{df[variable].median():.2f}")
    col3.metric("Desv. Estándar", f"{df[variable].std():.2f}")

    # --- MÓDULO 3: VISUALIZACIÓN ---
    st.divider()
    st.header("3. Visualización de Distribución")
    
    # Creamos dos columnas para los gráficos
    col_graf1, col_graf2 = st.columns(2)
    
    with col_graf1:
        st.subheader("Histograma y KDE")
        fig_hist, ax_hist = plt.subplots()
        import seaborn as sns # Importación local por seguridad
        sns.histplot(df[variable], kde=True, ax=ax_hist, color="skyblue")
        ax_hist.set_title("Distribución de Frecuencias")
        st.pyplot(fig_hist)

        with col_graf2:
        st.subheader("Boxplot (Valores Atípicos)")
        fig_box, ax_box = plt.subplots()
        sns.boxplot(x=df[variable], ax=ax_box, color="lightcoral")
        ax_box.set_title("Identificación de Outliers")
        st.pyplot(fig_box)

        # --- MÓDULO 4: INFERENCIA ESTADÍSTICA (IA BÁSICA) ---
    st.divider()
    st.header("4. Análisis de Normalidad")
    
    from scipy.stats import shapiro
    
    stat, p = shapiro(df[variable])
    
    st.write(f"**Resultado de la prueba Shapiro-Wilk:** p-valor = {p:.4f}")
    
    if p > 0.05:
        st.success("🤖 La IA determina: Los datos parecen seguir una Distribución Normal.")
        st.info("Sugerencia: Puedes usar pruebas paramétricas (como la Prueba Z o T).")
    else:
        st.warning("🤖 La IA determina: Los datos NO siguen una Distribución Normal.")
        st.info("Sugerencia: Considera usar pruebas no paramétricas o revisar los outliers.")