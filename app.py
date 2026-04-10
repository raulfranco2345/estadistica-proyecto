
import streamlit as st
import pandas as pd
import numpy as np

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