
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Estadística e IA - UP Chiapas", layout="wide")
st.title("🚀 Proyecto Final: Análisis Estadístico e IA")
st.caption("Autor: Franco Córdova Fabricio Raúl")
# --- SIDEBAR: IDENTIDAD (Commit 9 y 10) ---
with st.sidebar:
    st.image("https://www.upchiapas.edu.mx/images/logo_up.png", width=200)
    st.header("⚙️ Panel de Control")
    st.divider()
    st.subheader("🎨 Personalización")
    color_graf = st.color_picker("Color de identidad visual:", "#3498db")
    st.info("Autor: Franco Córdova Fabricio Raúl | ID: 253393")
# --- MÓDULO 7: REFLEXIÓN (Commit 8) ---
st.divider()
st.header("7. Reflexión del Proceso Creativo")
with st.expander("Ver preguntas de reflexión"):
    st.markdown("""
    * **1. ¿Qué limitaciones encontraste?** La IA presenta errores de indentación y requiere conocimiento técnico.
    * **2. ¿Cómo verificaste la precisión?** Se contrastaron los resultados de la 'Prueba Z' manual con librerías estándar.
    * **3. Impacto ético:** Es vital la supervisión humana para no aceptar conclusiones automáticas erróneas.
    """)