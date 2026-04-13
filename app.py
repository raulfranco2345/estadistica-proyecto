
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

with st.sidebar:
    st.image("https://www.upchiapas.edu.mx/images/logo_up.png", width=200)
    st.header("⚙️ Panel de Control")
    color_graf = st.color_picker("Color de los gráficos:", "#3498db")
    st.info("Autor: Fabricio Raúl Franco Córdova")

st.set_page_config(page_title="Estadística e IA - UP Chiapas", layout="wide")
st.title("🚀 Proyecto Final: Análisis Estadístico e IA")
st.markdown("### Estudiante: Franco Córdova Fabricio Raúl | ID: 253393")

# Datos base para que los commits tengan algo que procesar
df = pd.DataFrame(np.random.normal(50, 10, 100), columns=["Variable"])
variable = "Variable"

st.header("3. Visualización y Explorador")
tab1, tab2, tab3 = st.tabs(["Distribución", "Valores Atípicos", "Dispersión"])
with tab1:
    fig1, ax1 = plt.subplots(); sns.histplot(df[variable], kde=True, ax=ax1, color=color_graf); st.pyplot(fig1)
with tab2:
    fig2, ax2 = plt.subplots(); sns.boxplot(x=df[variable], ax=ax2, color=color_graf); st.pyplot(fig2)
with tab3:
    fig3, ax3 = plt.subplots(); ax3.scatter(df.index, df[variable], color=color_graf); st.pyplot(fig3)

with st.expander("🔍 Explorador de datos"):
    busqueda = st.number_input("Buscar valor:", value=0.0)
    st.write(f"Coincidencias: {len(df[df[variable].round(1) == round(busqueda, 1)])}")

st.header("5. Documentación y Reflexión Ética")
with st.expander("Preguntas sobre el proceso creativo"):
    st.markdown("""
    **1. ¿Limitaciones?** Errores de lógica en la IA que requieren revisión.
    **2. ¿Validación?** Comparación de cálculos con Excel y manuales.
    **3. ¿Ética?** Uso responsable de la IA como apoyo, no como autor total.
    """)

    if st.checkbox("Mostrar manual de uso (README)"):
    st.markdown("""
    ### Guía Rápida
    1. Carga tus datos en el sidebar.
    2. Personaliza el color.
    3. Analiza los gráficos y el explorador.
    """)

st.caption("Versión Final 1.0.0 - UP Chiapas")