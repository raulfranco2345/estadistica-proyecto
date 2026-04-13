
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import shapiro

# 1. CONFIGURACIÓN DE PÁGINA (Commit 14: Optimización de carga)
st.set_page_config(page_title="Estadística e IA - UP Chiapas", layout="wide", page_icon="📊")

# --- SIDEBAR: CONFIGURACIÓN (Commit 9 y 10: Interfaz y Color) ---
with st.sidebar:
    st.image("https://www.upchiapas.edu.mx/images/logo_up.png", width=200)
    st.header("⚙️ Panel de Control")
    
    opcion = st.radio(
        "Origen de los datos:", 
        ["Generar datos sintéticos", "Subir archivo CSV"]
    )
    
    st.divider()
    st.subheader("🎨 Personalización")
    color_graf = st.color_picker("Color de identidad visual:", "#3498db")
    
    st.divider()
    st.info("Software desarrollado para la asignatura de Estadística e IA.")
    st.caption("Autor: Franco Córdova Fabricio Raúl")

# --- TÍTULO Y CRÉDITOS ---
st.title("🚀 Proyecto Final: Análisis Estadístico e IA")
st.markdown("### Estudiante: Franco Córdova Fabricio Raúl | ID: 253393")

# --- MÓDULO 1: CARGA DE DATOS ---
st.header("1. Gestión de Datos")
df = None

if opcion == "Generar datos sintéticos":
    datos_base = np.random.normal(loc=50, scale=10, size=100)
    df = pd.DataFrame(datos_base, columns=["Variable_Analizada"])
    st.success("✅ Datos generados mediante Distribución Normal.")
else:
    archivo = st.file_uploader("Cargar dataset (CSV)", type=["csv"])
    if archivo:
        df = pd.read_csv(archivo)
        st.success("✅ Dataset cargado correctamente.")

if df is not None:
    variable = df.columns[0]
    
    # Commit 12: Buscador de datos/Filtro rápido
    with st.expander("🔍 Explorador de datos"):
        busqueda = st.number_input("Buscar valor específico en la muestra:", value=0.0)
        coincidencias = df[df[variable].round(2) == round(busqueda, 2)]
        if not coincidencias.empty:
            st.write(f"Se encontraron {len(coincidencias)} coincidencias.")
            st.dataframe(coincidencias)
        else:
            st.write("No hay coincidencias exactas.")

    # --- MÓDULO 2: ESTADÍSTICA ---
    st.divider()
    st.header("2. Métricas Descriptivas")
    c1, c2, c3 = st.columns(3)
    c1.metric("Media Aritmética", f"{df[variable].mean():.2f}")
    c2.metric("Mediana", f"{df[variable].median():.2f}")
    c3.metric("Desviación Estándar", f"{df[variable].std():.2f}")

    # --- MÓDULO 3: VISUALIZACIÓN (Commit 11: Dispersión) ---
    st.divider()
    st.header("3. Análisis Visual Avanzado")
    tab1, tab2, tab3 = st.tabs(["Distribución", "Valores Atípicos", "Dispersión"])
    
    with tab1:
        fig1, ax1 = plt.subplots()
        sns.histplot(df[variable], kde=True, ax=ax1, color=color_graf)
        st.pyplot(fig1)
    with tab2:
        fig2, ax2 = plt.subplots()
        sns.boxplot(x=df[variable], ax=ax2, color=color_graf)
        st.pyplot(fig2)
    with tab3:
        fig3, ax3 = plt.subplots()
        ax3.scatter(df.index, df[variable], alpha=0.5, color=color_graf)
        ax3.set_title("Dispersión Secuencial")
        st.pyplot(fig3)

    # --- MÓDULO 4 Y 5: INFERENCIA Y PRUEBA Z ---
    st.divider()
    st.header("4. Inferencia Estadística")
    
    stat, p = shapiro(df[variable])
    if p > 0.05:
        st.success(f"Probabilidad de Normalidad: {p:.4f} (Datos Normales)")
    else:
        st.warning(f"Probabilidad de Normalidad: {p:.4f} (Datos No Normales)")

    st.subheader("Prueba de Hipótesis (Z-Test)")
    colz1, colz2 = st.columns(2)
    with colz1:
        mu_h0 = st.number_input("Media Hipotética (μ₀):", value=50.0)
        conf = st.select_slider("Confianza:", options=[0.90, 0.95, 0.99], value=0.95)
    
    z_crit = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}[conf]
    z_calc = (df[variable].mean() - mu_h0) / (df[variable].std() / np.sqrt(len(df)))
    
    with colz2:
        st.write(f"Z Calculado: `{z_calc:.4f}` | Z Crítico: `{z_crit}`")
        if abs(z_calc) > z_crit:
            st.error("Resultado: Rechazo de Hipótesis Nula")
        else:
            st.success("Resultado: No se rechaza Hipótesis Nula")

    # --- MÓDULO 6: EXPORTACIÓN ---
    st.divider()
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Descargar Reporte CSV", data=csv, file_name='analisis_upchiapas.csv')

# --- MÓDULO 7: REFLEXIÓN (Commit 15: Ajustes de Redacción) ---
st.divider()
st.header("5. Documentación y Reflexión Ética")
with st.expander("Preguntas sobre el proceso creativo"):
    st.markdown(f"""
    **Estudiante:** {st.session_state.get('user_name', 'Fabricio Raúl Franco Córdova')}
    
    * **Limitaciones técnicas:** Se detectó que la IA requiere supervisión constante en la estructura de control de flujo de Streamlit para evitar errores de ejecución.
    * **Validación de resultados:** Se contrastaron las métricas de la librería Pandas con cálculos manuales para asegurar precisión total en el reporte académico.
    * **Ética Profesional:** El uso responsable de la IA implica entender la matemática detrás del código, no solo ejecutar scripts generados automáticamente.
    """)

# Commit 13: README dinámico al final
if st.checkbox("Mostrar manual de uso (README)"):
    st.markdown("""
    ### Instrucciones del Software
    1. Seleccione el método de entrada de datos en el panel izquierdo.
    2. Ajuste el color visual de su preferencia.
    3. Analice las métricas y gráficos generados automáticamente.
    4. Realice sus pruebas de hipótesis ajustando la media y confianza.
    """)