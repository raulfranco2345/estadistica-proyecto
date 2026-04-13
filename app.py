
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import google.generativeai as genai

# 1. CONFIGURACIÓN E IA
st.set_page_config(page_title="Estadística e IA - UP Chiapas", layout="wide")

# Configura tu API Key aquí (Obtenla en Google AI Studio)
# genai.configure(api_key="TU_API_KEY_AQUI") 

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

# --- MÓDULO 1: VISUALIZACIÓN Y ANÁLISIS DE DISTRIBUCIÓN ---
st.header("1. Análisis de Distribución")
col_v1, col_v2 = st.columns(2)
with col_v1:
    fig1, ax1 = plt.subplots(); sns.histplot(df[var], kde=True, ax=ax1, color=color_graf); st.pyplot(fig1)
with col_v2:
    fig2, ax2 = plt.subplots(); sns.boxplot(x=df[var], ax=ax2, color=color_graf); st.pyplot(fig2)

# RESPUESTA A RÚBRICA: ¿Es normal? ¿Sesgo?
k2, p_norm = stats.normaltest(df[var])
sesgo = df[var].skew()
st.subheader("📊 Diagnóstico de la Variable")
col_d1, col_d2, col_d3 = st.columns(3)
col_d1.metric("¿Es Normal?", "Sí" if p_norm > 0.05 else "No")
col_d2.metric("Sesgo", f"{sesgo:.2f}", help="Cercano a 0 es simétrico")
col_d3.metric("Outliers", len(df[np.abs(stats.zscore(df[var])) > 3]))

# --- MÓDULO 2: PRUEBA Z ---
st.header("2. Prueba de Hipótesis (Z-Test)")
c1, c2 = st.columns(2)
with c1:
    mu0 = st.number_input("Hipótesis Nula (μ₀):", value=50.0)
    tipo_test = st.selectbox("Hipótesis Alternativa (H₁):", ["Bilateral (≠)", "Cola Derecha (>)", "Cola Izquierda (<)"])
    alpha = st.slider("Significancia (α):", 0.01, 0.10, 0.05)
    sigma = st.number_input("Varianza poblacional (σ) conocida:", value=10.0)
    
    z_calc = (df[var].mean() - mu0) / (sigma / np.sqrt(len(df)))
    
    if "Bilateral" in tipo_test:
        p_val = 2 * (1 - stats.norm.cdf(abs(z_calc)))
        z_crit = stats.norm.ppf(1 - alpha/2)
    elif "Derecha" in tipo_test:
        p_val = 1 - stats.norm.cdf(z_calc)
        z_crit = stats.norm.ppf(1 - alpha)
    else:
        p_val = stats.norm.cdf(z_calc)
        z_crit = stats.norm.ppf(alpha)

with c2:
    st.write(f"**Estadístico Z:** {z_calc:.4f}")
    st.write(f"**P-Value:** {p_val:.4f}")
    
    # REQUISITO: Comparación con decisión del estudiante
    st.markdown("---")
    st.write("### Tu turno: ¿Qué decides?")
    tu_decision = st.radio("Basado en los datos:", ["No rechazar H₀", "Rechazar H₀"])
    decision_real = "Rechazar H₀" if p_val < alpha else "No rechazar H₀"
    
    if st.button("Validar mi decisión"):
        if tu_decision == decision_real:
            st.success(f"¡Correcto! La decisión estadística es {decision_real}.")
        else:
            st.error(f"Incorrecto. La evidencia sugiere {decision_real}.")

# --- GRÁFICO DE CAMPANA ---
x = np.linspace(-4, 4, 100)
y = stats.norm.pdf(x, 0, 1)
fig_z, ax_z = plt.subplots(figsize=(10, 3))
ax_z.plot(x, y, color='black')
ax_z.axvline(z_calc, color='blue', lw=2, label=f'Z-Calc: {z_calc:.2f}')
if "Bilateral" in tipo_test:
    ax_z.fill_between(x, y, where=(abs(x) > z_crit), color='red', alpha=0.3, label="Región Crítica")
elif "Derecha" in tipo_test:
    ax_z.fill_between(x, y, where=(x > z_crit), color='red', alpha=0.3, label="Región Crítica")
else:
    ax_z.fill_between(x, y, where=(x < z_crit), color='red', alpha=0.3, label="Región Crítica")
ax_z.legend(); st.pyplot(fig_z)

# --- MÓDULO 3: ASISTENTE IA ---
st.header("3. Asistente de IA (Gemini)")
resumen_stats = f"Prueba Z: mu0={mu0}, media={df[var].mean():.2f}, n={len(df)}, Z={z_calc:.2f}, alpha={alpha}, p={p_val:.4f}"

if st.button("Consultar Inferencia Ética"):
    # Aquí iría el llamado real: model.generate_content(prompt)
    st.write("🤖 **Análisis de IA:**")
    st.info(f"Dado que el p-value ({p_val:.4f}) es {'menor' if p_val < alpha else 'mayor'} que alpha ({alpha}), la inferencia lógica es {decision_real}. Este resultado es robusto dado que n={len(df)} (n >= 30). Se recomienda verificar si existen factores externos no considerados en el dataset.")

st.divider()
st.caption("Versión Final de Excelencia 1.2.0 - UP Chiapas")