
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import shapiro

# Configuración básica de la página (DEBE IR PRIMERO)
st.set_page_config(page_title="App de Estadística e IA - UP Chiapas", layout="wide")

# --- SIDEBAR: CONFIGURACIÓN (COMMIT 9) ---
with st.sidebar:
    # Logo oficial de la UP Chiapas
    st.image("https://www.upchiapas.edu.mx/images/logo_up.png", width=200)
    st.header("⚙️ Configuración")
    
    opcion = st.radio(
        "Selecciona el origen de los datos:", 
        ["Generar datos sintéticos", "Subir archivo CSV"]
    )
    
    st.divider()
    st.info("Desarrollado para la asignatura de Estadística e IA.")
    st.caption("Estudiante: Franco Córdova Fabricio Raúl")

# --- TÍTULO Y CRÉDITOS ---
st.title("📊 Documentación de Proceso Creativo")
st.markdown("### Estudiante: Franco Córdova Fabricio Raúl")
st.write("**Objetivo:** Evaluar las limitaciones de la IA en el desarrollo de software estadístico.")

st.divider()

# --- MÓDULO 1: CARGA DE DATOS ---
st.header("1. Carga de Datos")

# Inicializamos el DataFrame
df = None

if opcion == "Generar datos sintéticos":
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

# PROCESAMIENTO PRINCIPAL (Todo lo que depende de que existan datos)
if df is not None:
    variable = df.columns[0]
    
    st.subheader("Vista previa de los datos")
    st.dataframe(df.head(10))
    st.write(f"**Tamaño de la muestra (n):** {len(df)}")

    # --- MÓDULO 2: ESTADÍSTICA DESCRIPTIVA ---
    st.divider()
    st.header("2. Estadísticas Descriptivas")
    
    col_met1, col_met2, col_met3 = st.columns(3)
    col_met1.metric("Media", f"{df[variable].mean():.2f}")
    col_met2.metric("Mediana", f"{df[variable].median():.2f}")
    col_met3.metric("Desv. Estándar", f"{df[variable].std():.2f}")

    # --- MÓDULO 3: VISUALIZACIÓN ---
    st.divider()
    st.header("3. Visualización de Distribución")
    
    col_graf1, col_graf2 = st.columns(2)
    
    with col_graf1:
        st.subheader("Histograma y KDE")
        fig_hist, ax_hist = plt.subplots()
        sns.histplot(df[variable], kde=True, ax=ax_hist, color="skyblue")
        ax_hist.set_title("Distribución de Frecuencias")
        st.pyplot(fig_hist)

    with col_graf2:
        st.subheader("Boxplot (Valores Atípicos)")
        fig_box, ax_box = plt.subplots()
        sns.boxplot(x=df[variable], ax=ax_box, color="lightcoral")
        ax_box.set_title("Identificación de Outliers")
        st.pyplot(fig_box)

    # --- MÓDULO 4: INFERENCIA ESTADÍSTICA ---
    st.divider()
    st.header("4. Análisis de Normalidad")
    stat, p = shapiro(df[variable])
    st.write(f"**Resultado de la prueba Shapiro-Wilk:** p-valor = `{p:.4f}`")
    
    if p > 0.05:
        st.success("🤖 La IA determina: Los datos parecen seguir una Distribución Normal.")
    else:
        st.warning("🤖 La IA determina: Los datos NO siguen una Distribución Normal.")

    # --- MÓDULO 5: PRUEBA DE HIPÓTESIS (Prueba Z) ---
    st.divider()
    st.header("5. Prueba de Hipótesis (Z-Test)")
    
    col_z1, col_z2 = st.columns(2)
    with col_z1:
        mu_h0 = st.number_input("Ingresa la Media Hipotética (μ₀):", value=50.0)
        confianza = st.select_slider("Nivel de Confianza:", options=[0.90, 0.95, 0.99], value=0.95)

    valores_criticos = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}
    z_critico = valores_criticos[confianza]
    z_stat = (df[variable].mean() - mu_h0) / (df[variable].std() / np.sqrt(len(df)))
    
    with col_z2:
        st.write(f"**Estadístico Z calculado:** `{z_stat:.4f}`")
        st.write(f"**Valor crítico (z):** `{z_critico}`")
        if abs(z_stat) > z_critico:
            st.error("🔴 Rechazamos H₀: Hay una diferencia significativa.")
        else:
            st.success("🟢 No rechazamos H₀: No hay evidencia de diferencia significativa.")

    # --- MÓDULO 6: EXPORTACIÓN ---
    st.divider()
    st.header("6. Exportar Resultados")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(label="📥 Descargar datos en CSV", data=csv, file_name='analisis_estadistico.csv', mime='text/csv')

# --- MÓDULO 7: REFLEXIÓN (Este queda fuera del IF principal para que siempre se vea) ---
st.divider()
st.header("7. Reflexión del Proceso Creativo")
with st.expander("Ver preguntas de reflexión"):
    st.markdown("""
    **1. ¿Qué limitaciones encontraste en la IA durante el desarrollo?**
    *Respuesta:* La IA presenta errores de indentación y requiere conocimiento técnico para estructurar el flujo de Streamlit correctamente.
    
    **2. ¿Cómo verificaste la precisión de los cálculos estadísticos?**
    *Respuesta:* Se contrastaron los resultados de la 'Prueba Z' manual con la lógica de librerías estándar.
    
    **3. Impacto ético del uso de IA en software estadístico:**
    *Respuesta:* Es vital la supervisión humana para no aceptar conclusiones automáticas que podrían estar basadas en datos mal procesados.
    """)
    # --- MÓDULO 8: ANÁLISIS COMPARATIVO ---
    st.divider()
    st.header("8. Análisis Comparativo")
    
    comparativo = st.number_input("Valor de referencia para comparar:", value=50.0)
    
    # Creamos un gráfico de barras comparando la Media actual vs el valor de referencia
    fig_comp, ax_comp = plt.subplots()
    categorias = ['Media Actual', 'Referencia']
    valores = [df[variable].mean(), comparativo]
    ax_comp.bar(categorias, valores, color=['#3498db', '#e74c3c'])
    ax_comp.set_ylabel('Valor')
    ax_comp.set_title('Comparativa: Media vs Referencia')
    
    st.pyplot(fig_comp)