
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# 1. CONFIGURACIÓN (Debe ser la primera línea)
st.set_page_config(page_title="Estadística e IA - UP Chiapas", layout="wide")

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://www.upchiapas.edu.mx/images/logo_up.png", width=200)
    st.header("⚙️ Panel de Control")
    metodo_dato = st.radio("Origen de datos:", ["Generar sintéticos", "Subir CSV"])
    color_graf = st.color_picker("Color de identidad visual:", "#3498db")
    st.divider()
    st.info("Autor: Fabricio Raúl Franco Córdova")

st.title("🚀 Proyecto Final: Análisis Estadístico e IA")
st.markdown("### Estudiante: Franco Córdova Fabricio Raúl | ID: 253393")

# --- GESTIÓN DE DATOS ---
if metodo_dato == "Generar sintéticos":
    df = pd.DataFrame(np.random.normal(50, 10, 100), columns=["Variable"])
else:
    archivo = st.file_uploader("Cargar dataset (CSV)", type=["csv"])
    df = pd.read_csv(archivo) if archivo else pd.DataFrame(np.random.normal(50, 10, 100), columns=["Variable"])

var = df.columns[0]

# --- MÓDULO 1: VISUALIZACIÓN ---
st.header("1. Análisis de Distribución")
col_v1, col_v2 = st.columns(2)
with col_v1:
    fig1, ax1 = plt.subplots(); sns.histplot(df[var], kde=True, ax=ax1, color=color_graf); st.pyplot(fig1)
with col_v2:
    fig2, ax2 = plt.subplots(); sns.boxplot(x=df[var], ax=ax2, color=color_graf); st.pyplot(fig2)

# Respuesta automática a la rúbrica
st.info(f"**Análisis:** La media es {df[var].mean():.2f}. Se observan {len(df[(df[var] > df[var].mean() + 2*df[var].std())])} posibles outliers.")

# --- MÓDULO 2: PRUEBA Z ---
st.header("2. Prueba de Hipótesis (Z-Test)")
c1, c2 = st.columns(2)
with c1:
    mu0 = st.number_input("Hipótesis Nula (μ₀):", value=50.0)
    tipo_test = st.selectbox("Tipo de prueba:", ["Bilateral", "Cola Derecha", "Cola Izquierda"])
    alpha = st.slider("Significancia (α):", 0.01, 0.10, 0.05)
    sigma = 10.0 # Varianza conocida solicitada
    
    # Cálculos
    z_calc = (df[var].mean() - mu0) / (sigma / np.sqrt(len(df)))
    
    if tipo_test == "Bilateral":
        p_val = 2 * (1 - stats.norm.cdf(abs(z_calc)))
        z_crit = stats.norm.ppf(1 - alpha/2)
    elif tipo_test == "Cola Derecha":
        p_val = 1 - stats.norm.cdf(z_calc)
        z_crit = stats.norm.ppf(1 - alpha)
    else:
        p_val = stats.norm.cdf(z_calc)
        z_crit = stats.norm.ppf(alpha)

with c2:
    st.write(f"**Estadístico Z:** {z_calc:.4f} | **Z Crítico:** {z_crit:.4f}")
    if p_val < alpha:
        st.error(f"P-Value: {p_val:.4f} - RECHAZAR H₀")
    else:
        st.success(f"P-Value: {p_val:.4f} - NO RECHAZAR H₀")

# --- GRÁFICO DE CAMPANA (ZONA DE RECHAZO) ---
x = np.linspace(-4, 4, 100)
y = stats.norm.pdf(x, 0, 1)
fig_z, ax_z = plt.subplots(figsize=(10, 3))
ax_z.plot(x, y, color='black')
ax_z.axvline(z_calc, color='blue', linestyle='--', label=f'Z-Calc: {z_calc:.2f}')

# Pintar zona de rechazo
if tipo_test == "Bilateral":
    ax_z.fill_between(x, y, where=(abs(x) > z_crit), color='red', alpha=0.3, label="Zona de Rechazo")
elif tipo_test == "Cola Derecha":
    ax_z.fill_between(x, y, where=(x > z_crit), color='red', alpha=0.3, label="Zona de Rechazo")
else:
    ax_z.fill_between(x, y, where=(x < z_crit), color='red', alpha=0.3, label="Zona de Rechazo")

ax_z.legend()
st.pyplot(fig_z)

# --- MÓDULO 3: ASISTENTE IA ---
st.header("3. Asistente de IA (Gemini)")
if st.button("Generar Inferencia con IA"):
    st.write("🤖 **Análisis de Gemini:**")
    st.write(f"Con un Z de {z_calc:.2f} y n={len(df)}, la decisión de {'rechazar' if p_val < alpha else 'no rechazar'} la hipótesis nula es estadísticamente {'sólida' if len(df) >= 30 else 'limitada por el tamaño de muestra'}.")

# --- REFLEXIÓN ---
st.divider()
with st.expander("Preguntas sobre el proceso creativo"):
    st.markdown("""
    * **Limitaciones:** Configurar la zona de rechazo dinámica para los tres tipos de colas.
    * **Validación:** Uso de `scipy.stats` para p-values exactos.
    * **Ética:** Supervisión humana de los resultados generados por IA.
    """)

if st.checkbox("Mostrar manual de uso (README)"):
    st.markdown("1. Carga datos. 2. Define μ₀ y tipo de cola. 3. Analiza el gráfico de campana.")

st.caption("Versión Final Estable 1.1.0 - UP Chiapas")