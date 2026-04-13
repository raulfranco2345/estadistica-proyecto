
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Estadística e IA - UP Chiapas", layout="wide")
st.title("🚀 Proyecto Final: Análisis Estadístico e IA")
st.markdown("### Estudiante: Franco Córdova Fabricio Raúl | ID: 253393")

# Datos base para que los commits tengan algo que procesar
df = pd.DataFrame(np.random.normal(50, 10, 100), columns=["Variable"])
variable = "Variable"

st.header("5. Documentación y Reflexión Ética")
with st.expander("Preguntas sobre el proceso creativo"):
    st.markdown("""
    **1. ¿Limitaciones?** Errores de lógica en la IA que requieren revisión.
    **2. ¿Validación?** Comparación de cálculos con Excel y manuales.
    **3. ¿Ética?** Uso responsable de la IA como apoyo, no como autor total.
    """)